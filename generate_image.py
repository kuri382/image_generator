import random

import numpy as np
import pandas as pd
from PIL import Image, ImageDraw, ImageFont

MAX_STORY = 8
MAX_LEVEL = 5


def add_text_to_image(img, text, font_path, font_size, font_color, height, width, max_length=740):
    """
    画像内にテキストをペーストする処理（今回のプロジェクトでは使用せず）
    """
    position = (width, height)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
    if draw.textsize(text, font=font)[0] > max_length:
        while draw.textsize(text + "…", font=font)[0] > max_length:
            text = text[:-1]
        text = text + "…"

    draw.text(position, text, font_color, font=font)

    return img


def add_messages(background, test_day):
    """
    画像内に表示するテキストを生成する処理（今回のプロジェクトでは使用せず）
    """
    title = "Sample text"
    font_path = "fonts/mick-caster/Mick Caster.otf"
    font_size = 57
    font_color = (25, 160, 160)
    height = 15
    width = 30
    background = add_text_to_image(background, title, font_path, font_size, font_color, height, width)

    title = "Day " + str(test_day)
    font_path = "fonts/mick-caster/Mick Caster.otf"
    font_size = 57
    font_color = (25, 160, 160)
    height = 15
    width = 300
    background = add_text_to_image(background, title, font_path, font_size, font_color, height, width)

    test_param = 0

    title = "Sample parameter = " + str(test_param)
    font_path = "fonts/mick-caster/Mick Caster.otf"
    font_size = 30
    font_color = (25, 160, 160)
    height = 100
    width = 30
    background = add_text_to_image(background, title, font_path, font_size, font_color, height, width)

    title = "Sample parameter = " + str(test_param)
    font_path = "fonts/mick-caster/Mick Caster.otf"
    font_size = 30
    font_color = (255, 100, 70)
    height = 130
    width = 30
    background = add_text_to_image(background, title, font_path, font_size, font_color, height, width)

    title = "Sample text, sample text, sample text!"
    font_path = "fonts/mick-caster/Mick Caster.otf"
    font_size = 40
    font_color = (255, 100, 70)
    height = 950
    width = 30
    background = add_text_to_image(background, title, font_path, font_size, font_color, height, width)

    return background


def paste_image(background, image, story, level, x, y):
    """
    アイコン画像をペーストする処理
    """
    icon_path = image[story][level]
    image = Image.open(icon_path).copy()
    offset_x = image.size[0] - 561
    offset_y = image.size[1] - 280
    background.paste(image, (x - offset_x, y - offset_y), image)
    return background


def load_image():
    """
    参照元画像の読み込み
    """
    icons = np.zeros((MAX_STORY, MAX_LEVEL), dtype=object)
    for story in range(MAX_STORY):
        for level in range(MAX_LEVEL):
            icon_path = "img/input/story_{}_{}.png".format(story, level)
            icons[story][level] = icon_path
    return icons


def set_background_images():
    """
    全画像で共通の背景を生成する
    """
    background_path = "img/input/background.png"
    background = Image.open(background_path).copy()

    # background color
    background_color = Image.new("RGB", (1920, 1080), (87, 179, 110))
    background.paste(background_color, (0, 0))

    # ground images
    base_path = "img/input/base_0.png"
    base = Image.open(base_path).copy()
    background.paste(base, (0, 0), base)

    return background


def create_images(story, section, output_csv):
    """
    レベルごとの画像を生成し、画像に付随するメッセージ(src/message.csv)から
    全体画像に添付されるGF用のレベル情報を含むcsv(output.csv)を生成する
    画像はimg/outputに保存される
    """
    message_df = pd.read_csv("src/messages.csv")

    # load building images from folder
    icons = load_image()
    section_level = [0, 0, 0, 0]
    total_level = 4 * (MAX_LEVEL - 1)  # 4sections

    story_name = ""
    for i in section:
        story_name += str(i)

    past_levels = [0, 0, 0, 0]

    for level in range(total_level):
        background = set_background_images()

        selected_section = random.randrange(4)
        while section_level[selected_section] > (MAX_LEVEL - 2):
            selected_section = random.randrange(4)
        section_level[selected_section] += 1

        # buildings
        background = paste_image(background, icons, section[0], section_level[0], 900, 250)  # upper right
        background = paste_image(background, icons, section[1], section_level[1], 294, 552)  # upper left
        background = paste_image(background, icons, section[2], section_level[2], 1192, 396)  # lower right
        background = paste_image(background, icons, section[3], section_level[3], 586, 698)  # lower left

        message_column = 2
        value = section[selected_section] * (MAX_LEVEL - 1) + section_level[selected_section] - 1
        print(level, "selected_section", selected_section, "current_section=", value)
        position_info = ["奥", "左側", "右側", "手前"]
        level_message = (
            "{}の".format(position_info[selected_section])
            + message_df.iat[value, 1]
            + "区画のニュースです！ "
            + message_df.iat[value, message_column]
        )
        print(level_message)
        level_population = message_df.iat[value, 6]
        level_education = message_df.iat[value, 7]
        level_health = message_df.iat[value, 8]
        level_nature = message_df.iat[value, 9]

        past_levels[0] += level_population
        past_levels[1] += level_education
        past_levels[2] += level_health
        past_levels[3] += level_nature

        output_csv = output_csv.append(
            {
                "title_number": story,
                "message": level_message,
                "level": level,
                "character": message_df.iat[value, 3],
                "character_message": message_df.iat[value, 4],
                "character_img": message_df.iat[value, 5],
                "level_population": past_levels[0],
                "level_education": past_levels[1],
                "level_health": past_levels[2],
                "level_nature": past_levels[3],
            },
            ignore_index=True,
        )

        print("levels", past_levels)

        # put tree
        trees_path = "img/input/front_trees.png"
        trees = Image.open(trees_path).copy()
        background.paste(trees, (0, 635), trees)

        # put boards
        boards_path = "img/input/front_boards.png"
        boards = Image.open(boards_path).copy()
        background.paste(boards, (650, 330), boards)

        # put text
        # background = messages(background,title)

        png_filename = "output_for_slack_app/img/story_{}_{}.png".format(story, level)
        background.save(png_filename, quality=95)

        background = None
    return output_csv


if __name__ == "__main__":
    output = pd.DataFrame(
        columns=[
            "title_number",
            "message",
            "level",
            "character",
            "character_message",
            "character_img",
            "level_population",
            "level_education",
            "level_health",
            "level_nature",
        ]
    )

    output = create_images(0, [1, 0, 3, 4], output)
    output = create_images(1, [2, 4, 5, 6], output)
    output = create_images(2, [0, 2, 3, 4], output)
    output = create_images(3, [5, 1, 2, 6], output)

    output.to_csv("output_for_slack_app/output.csv", header=False)
