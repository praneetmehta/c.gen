import requests
from cgitb import text
from PIL import Image, ImageFont, ImageDraw
from image_generator.entities.image_config import ImageConfig
from image_generator.entities.request import Request

from image_generator.entities.text_config import TextConfig


def generate_image(request: Request, text_config: TextConfig, bg_config: ImageConfig) -> bool:
    if request.content.use_image:
        tmp_image_path = request.output_path.replace('frames', 'tmp_bg_frames')
        img_url = request.content.content_image_url
        if request.content.content_image_url == None:

        img_data = requests.get(request.content.content_image_url).content
        with open(tmp_image_path, 'wb') as handler:
            handler.write(img_data)
        image = Image.open(tmp_image_path)
        image = image.resize((bg_config.resolution.X, bg_config.resolution.Y))

        source = image.split()

        R, G, B = 0, 1, 2
        constant = 3.5 # constant by which each pixel is divided

        Red = source[R].point(lambda i: i/constant)
        Green = source[G].point(lambda i: i/constant)
        Blue = source[B].point(lambda i: i/constant)

        image = Image.merge(image.mode, (Red, Green, Blue))
    else:
        image = Image.new('RGB', 
                    (bg_config.resolution.X, bg_config.resolution.Y), 
                    (bg_config.bg_color.X, bg_config.bg_color.Y, bg_config.bg_color.Z))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(text_config.font.value,text_config.size)
    text_to_use_split = request.content.content.split()
    text_to_use = (' ').join(text_to_use_split[0:1]).strip() + '\n\n' + (' ').join(text_to_use_split[1:]).strip()
    x, y = draw.textsize(text_to_use, font=font)

    
    if x > bg_config.resolution.X-200:
        words = text_to_use.split(' ')
        split_at = int(4*len(words)/9)
        text_to_use = (' ').join(words[0:split_at]) + '\n\n' + (' ').join(words[split_at:])
        x, y = draw.textsize(text_to_use, font=font)
        
    x_offset = text_config.offset_percent.X*bg_config.resolution.X/100
    y_offset = text_config.offset_percent.Y*bg_config.resolution.Y/100

    if text_config.align == "center":
        x_offset = (bg_config.resolution.X-x)/2
        y_offset = (bg_config.resolution.Y-y)/2
    elif text_config.align == "vcenter":
        y_offset = (bg_config.resolution.Y-y)/2
    elif text_config.align == "hcenter":
        x_offset = (bg_config.resolution.X-x)/2
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
    return True