
@slack_app.message("send_weekly_feedback")
def send_weekly_feedback(say):
    say(
        {
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Weekly Feedback送信用のモーダルを開きます"
                    }
                },
                {
                    "type": "actions",
                    "elements": [
                        {
                            "type": "button",
                            "text": {
                                "type": "plain_text",
                                "text": "入力画面を開く",
                                "emoji": True
                            },
                            "value": "click_me_123",
                            "action_id": "open_weekly_feedback_modal"
                        }
                    ]
                }
            ]
        }
    )

@slack_app.action("open_weekly_feedback_modal")
def edit_weekly_feedback(ack, body, client):
    ack()
    client.views_open(
        trigger_id=body["trigger_id"],
        view={
            "type": "modal",
            "title": {
                "type": "plain_text",
                "text": "Weekly Feedback送信画面",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "送信する",
                "emoji": True
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel",
                "emoji": True
            },
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "送信する文章を入力してください"
                    }
                },
                {
                    "type": "input",
                    "block_id": "main_text",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "説明文章",
                        "emoji": True
                    }
                },
                {
                    "type": "input",
                    "block_id": "image_url",
                    "element": {
                        "type": "plain_text_input",
                        "action_id": "input-action"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "送信する画像のURL",
                        "emoji": True
                    }
                }
            ]
        }
    )
    
    

@slack_app.action("modal_plain_text_input-actio")
def send_weekly_feedback(say, body, client):
    client.chat_postMessage(
        channel=os.environ["SLACK_PROJECT_CHANNEL_ID"],
        text="ウィークリーフィードバックの投稿です！",
        blocks="message",
    )

