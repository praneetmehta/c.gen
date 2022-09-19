import requests
import os
from cgitb import text
from PIL import Image, ImageFont, ImageDraw
from content_provider.config.frame import TextBlock
from image_generator.entities.image_config import ImageConfig
from image_generator.entities.request import Request

from image_generator.entities.text_config import TextConfig


def generate_image(request: Request) -> bool:
    tmp_image_path = request.output_path.replace('frames', 'tmp_bg_frames')
    image_config : ImageConfig = request.content.image_content.image_config
    if request.content.use_image:
        if request.content.image_content.is_image_local:
            os.system("cp {} {}".format(request.content.image_content.content_image_url, tmp_image_path))
        else:
            img_url = request.content.image_content.content_image_url
            img_data = requests.get(img_url).content
            with open(tmp_image_path, 'wb') as handler:
                handler.write(img_data)
        image = Image.open(tmp_image_path)
        image = image.resize((image_config.resolution.X, image_config.resolution.Y))

        if image_config.darken:
            source = image.split()

            R, G, B = 0, 1, 2
            constant = 2.8 # constant by which each pixel is divided

            Red = source[R].point(lambda i: i/constant)
            Green = source[G].point(lambda i: i/constant)
            Blue = source[B].point(lambda i: i/constant)

            image = Image.merge(image.mode, (Red, Green, Blue))
    else:
        image = Image.new('RGB', 
                    (image_config.resolution.X, image_config.resolution.Y), 
                    (image_config.bg_color.X, image_config.bg_color.Y, image_config.bg_color.Z))
    draw = ImageDraw.Draw(image)
    if (request.content.textual_content != None):
        for text_block in request.content.textual_content:
            text_config = text_block.text_config
            font = ImageFont.truetype(text_config.font.value,text_config.size)
            # text_to_use_split = request.content.content.split(' ')
            text_to_use = text_block.text.strip()
            x, y = draw.textsize(text_to_use, font=font)

            line_break_condition = image_config.resolution.X-200
            if text_config.align == "":
                line_break_condition = image_config.resolution.X*(1-2*text_config.offset_percent.X/100)
            else:
                line_break_condition = image_config.resolution.X*0.8
            if x > line_break_condition:
                splits = int(x/line_break_condition)+1
                words = text_to_use.split(' ')
                lines_to_use = [(' ').join(words[int(split/splits*len(words)):int((1+split)/splits*len(words))]) for split in range(splits)]
                # words = text_to_use.split(' ')
                # split_at = int(4*len(words)/9)
                # text_to_use = (' ').join(words[0:split_at]) + '\n'*text_config.split_by_lines + (' ').join(words[split_at:])
                text_to_use = ('\n'*text_config.split_by_lines).join(lines_to_use)
                x, y = draw.textsize(text_to_use, font=font)
            
            x_offset = text_config.offset_percent.X*image_config.resolution.X/100
            y_offset = text_config.offset_percent.Y*image_config.resolution.Y/100

            if text_config.align == "center":
                x_offset = (image_config.resolution.X-x)/2
                y_offset = (image_config.resolution.Y-y)/2
            elif text_config.align == "vcenter":
                y_offset = (image_config.resolution.Y-y)/2
            elif text_config.align == "hcenter":
                x_offset = (image_config.resolution.X-x)/2
            draw.text((
                    int(x_offset), 
                    int(y_offset)
                ),
                text_to_use,
                (
                    text_config.color.X, 
                    text_config.color.Y, 
                    text_config.color.Z
                ),
                font
            )

    image.save(request.output_path)
    if request.content.use_image and request.content.image_content.is_image_local:
        os.system("rm {}".format(request.output_path.replace('frames', 'tmp_bg_frames')))
    return True