import os
from datetime import datetime, timedelta, timezone

import slack_sdk
from model import Answer, DailyImage, User, UserLevel, UserMeeting
from setting import session
from slack_bolt import App
from slack_templates import slack_dicts
from sqlalchemy import func
from sqlalchemy.sql import exists

slack_app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)


def calculate_point(user_id):
    """
    前日の会議数及びアンケート回答数から、回答率を計算しDBに保存する
    Args:
        user_id(int):参加者のユニークid
    Returns:
        None
    """
    # 前日の会議有無を確認
    jst = timezone(timedelta(hours=9))
    now = datetime.now(tz=jst)
    yesterday = datetime.strftime((now - timedelta(days=1)), "%Y-%m-%d")
    user_meetings = (
        session.query(UserMeeting)
        .filter(UserMeeting.user_id == user_id)
        .filter(func.Date(UserMeeting.start_time) == yesterday)
        .all()
    )

    # 前日の会議数及び回答数をカウント
    count_mtg = 0
    count_answer = 0
    for user_meeting in user_meetings:
        count_mtg += 1
        answer = session.query(Answer).filter(Answer.user_meeting_id == user_meeting.id).first()
        if answer.submitted_time is not None:
            count_answer += 1

    if count_mtg == 0:
        answer_rate = 0
    else:
        answer_rate = float(count_answer / count_mtg)

    ANSWER_RATE_THRESHOLD = 0.6
    if answer_rate >= ANSWER_RATE_THRESHOLD:
        user_level = session.query(UserLevel).filter(UserLevel.user == user_id).one()
        user_level.point = 1 + user_level.point
        session.add(user_level)
        session.commit()
        session.close()
    return


def create_daily_message(user_id, user_slack_id):
    """
    前日の回答率から、現在のレベルを計算し画像を送信する
    Args:
        user_id(int):参加者のユニークid
    Returns:
        message(dict):送信するview
    """
    user_level = session.query(UserLevel).filter(UserLevel.user == user_id).one()
    LEVEL_MAX = 15
    LEVEL_THRESHOLD = 3
    current_level = user_level.point // LEVEL_THRESHOLD
    story = user_level.selected_story

    # レベル上限以上には増加しないように制限
    if current_level >= LEVEL_MAX:
        current_level = LEVEL_MAX

    user_level.level = current_level
    session.add(user_level)
    session.commit()
    session.close()

    # 送信する情報の参照
    info_id = (16 * story) + current_level  # 一列に保存されたlevel情報から、各storyごとの情報を参照
    daily_info = session.query(DailyImage).filter(DailyImage.id == info_id).one()

    message = slack_dicts.daily_feedback(user_slack_id)
    if daily_info.character_img is not None:
        message.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "*{}の声が聞こえます！* \n {}".format(daily_info.character, daily_info.character_message),
                },
                "accessory": {
                    "type": "image",
                    "image_url": os.environ["IMG_BASE_URL"] + "characters/" + daily_info.character_img,
                    "alt_text": "住民からの声"
                }
            }
        )

    # 送信するviewの生成
    url = os.environ["IMG_BASE_URL"] + "daily_images/story_{}_{}.png".format(story, current_level)
    message[2]["image_url"] = url
    session.close()

    return message


def daily():
    """
    平日毎朝10時に送信する処理
    - ストーリー選択済ユーザーに対して、デイリーフィードバックを送信
    - ストーリー未選択ユーザーに対して、選択用モーダルを送信
    Args:
    Returns:
    """
    users = session.query(User).filter(User.google_access_token.isnot(None)).all()
    for user in users:
        user_level_exist = session.query(exists().where(UserLevel.user == user.id)).scalar()
        channel = user.slack_dm_channel_id

        if user_level_exist:
            calculate_point(user.id)
            try:
                message = create_daily_message(user.id, user.slack_id)

                slack_app.client.chat_postMessage(
                    token=slack_app._token,
                    text="",
                    blocks=message,
                    channel=channel,
                )
            except slack_sdk.errors.SlackApiError:
                slack_app.client.chat_postMessage(
                    token=slack_app._token,
                    text="エラー：本日のニュースが見つかりませんでした、お手数ですが管理者にご連絡ください",
                    channel=channel,
                )

        else:
            message = slack_dicts.gf_start_message()
            slack_app.client.chat_postMessage(
                token=slack_app._token,
                text="",
                blocks=message,
                channel=channel,
            )

    session.close()

    return


def weekly():
    users = session.query(User).all()
    for user in users:
        slack_app.client.chat_postMessage(
            token=slack_app._token,
            text="weekly_feedback テストです",
            channel=user.slack_dm_channel_id,
        )
    return
