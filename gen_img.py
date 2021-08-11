import numpy as np
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import random


MAX_STORY = 6
MAX_LEVEL = 5

def add_text_to_image(img, text, font_path, font_size, font_color, height, width, max_length=740):
    position = (width, height)
    font = ImageFont.truetype(font_path, font_size)
    draw = ImageDraw.Draw(img)
    if draw.textsize(text, font=font)[0] > max_length:
        while draw.textsize(text + '…', font=font)[0] > max_length:
            text = text[:-1]
        text = text + '…'

    draw.text(position, text, font_color, font=font)

    return img

def messages(background, test_day):
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
    icon_path = image[story][level]
    image = Image.open(icon_path).copy()
    offset_x = image.size[0]-561
    offset_y = image.size[1]-280
    background.paste(image, (x-offset_x, y-offset_y), image)
    return background

def load_image():
    icons = np.zeros((MAX_STORY,MAX_LEVEL),dtype=object)
    for story in range(MAX_STORY):
        for level in range(MAX_LEVEL):
            icon_path = 'img/input/story_{}_{}.png'.format(story,level)
            icons[story][level] = icon_path
    return icons


def main():
    background_path = 'img/input/background.png'
    background = Image.open(background_path).copy()

    # background color
    background_color = Image.new('RGB', (1920, 1080), (87,179,110))
    background.paste(background_color, (0, 0))

    # ground images
    base_path = 'img/input/base_0.png'
    base = Image.open(base_path).copy()
    background.paste(base, (0, 0), base)

    # load building images from folder
    icons = load_image()
    section = [3,1,5,4]
    story = 2
    section_level = [0,0,0,0]
    total_level = 4 * (MAX_LEVEL-1) # 4sections

    story_name = ''
    for i in section:
        story_name += str(i)

    for level in range(total_level):
        selected_section = random.randrange(4)
        while section_level[selected_section] > (MAX_LEVEL-2):
            selected_section = random.randrange(4)
        section_level[selected_section] += 1

        # buildings
        background = paste_image(background, icons, section[0], section_level[0], 895, 260) # upper right
        background = paste_image(background, icons, section[1], section_level[1], 300, 560) # upper left
        background = paste_image(background, icons, section[2], section_level[2], 1190, 405) # bottom right
        background = paste_image(background, icons, section[3], section_level[3], 590, 705) # bottom left
        
        # front decorations
        trees_path = 'img/input/front_trees.png'
        trees = Image.open(trees_path).copy()
        background.paste(trees, (0, 635), trees)
        
        boards_path = 'img/input/front_boards.png'
        boards = Image.open(boards_path).copy()
        background.paste(boards, (650, 330), boards)

        # put text
        # background = messages(background,title)

        """
        title = (str(section[0])+"-"+str(section_level[0])+"_"
                +str(section[1])+"-"+str(section_level[1])+"_"
                +str(section[2])+"-"+str(section_level[2])+"_"
                +str(section[3])+"-"+str(section_level[3]))
        """
        png_filename = 'img/output/story_{}_{}.png'.format(story, level)
        background.save(png_filename, quality=95)

if __name__=="__main__":
    main()