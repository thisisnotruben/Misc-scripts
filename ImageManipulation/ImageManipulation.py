#!/usr/bin/env python3

from os.path import join

from PIL import Image, ImageFont, ImageDraw

_font_dir = "magofonts"


def _get_frame_size(img_width, img_height, hvframes=()):
    width = int(img_width / hvframes[0])
    height = int(img_height / hvframes[1])
    return width, height


def fill_bg(input_path, output_path, color=(21, 21, 21)):
    """Fills image with background color"""
    with Image.open(input_path) as img:
        backgroud = Image.new("RGBA", (img.width, img.height), color)
        backgroud.paste(img, (0, 0), img)
        backgroud.save(output_path)
        backgroud.close()


def text_grid(input_path, output_path, hvframes=(), offset=(1, 1), text_color=(255, 0, 255, 255),
              text_font=ImageFont.truetype(join(_font_dir, "mago1.ttf"), 32), start_count=0):
    """Enumerates image in a grid like fashion per frame"""
    with Image.open(input_path) as img:
        draw = ImageDraw.Draw(img)
        width, height = _get_frame_size(img.width, img.height, hvframes)
        count = start_count
        for y in range(0, img.height, height):
            for x in range(0, img.width, width):
                draw.text((x + offset[0], y + offset[1]), str(count), fill=text_color, font=text_font)
                count += 1
        img.save(output_path)


def make_grid(input_path, output_path, hvframes=(), line_width=1, offset=(1, 1), color=(0, 255, 0)):
    """Draws a grid on the image."""
    with Image.open(input_path) as img:
        draw = ImageDraw.Draw(img)
        width, height = _get_frame_size(img.width, img.height, hvframes)
        for x in range(0, img.width, width):
            line = ((x + offset[0], 0), (x + offset[0], img.height))
            draw.line(line, color, line_width)
        for y in range(0, img.height, height):
            line = ((0, y + offset[1]), (img.width, y + offset[1]))
            draw.line(line, color, line_width)
        img.save(output_path)


def crop_frame(input_path, output_path, hvframes=(), frame=()):
    """Crops Image; hvframes/frame parameters are tuples, frame starts at 0"""
    with Image.open(input_path) as img:
        width, height = _get_frame_size(img.width, img.height, hvframes)
        x = width * frame[0]
        y = height * frame[1]
        sprite = img.crop((x, y, x + width, y + height))
        final = Image.new("RGBA", (width, height))
        final.paste(sprite, (0, 0))
        final.save(output_path)
        final.close()
