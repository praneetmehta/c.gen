from __future__ import annotations

from dataclasses import dataclass
import json
from types import SimpleNamespace
from typing import List
from image_generator.entities.font_enum import Font
from image_generator.entities.image_config import ImageConfig

from image_generator.entities.text_config import TextConfig



class TextBlock:
    _default_style_config : TextConfig | None = None

    def __init__(self, text="", style_config : TextConfig | None = None):
        self.text = text
        self.text_config = TextBlock.get_default_text_config(style_config)


    @staticmethod
    def get_default_text_config(config : TextConfig | None):
        if config != None:
            return config
        if TextBlock._default_style_config == None:
            txt_config = TextConfig.load_text_config_from_file("default_text_config.json")
            TextBlock._default_style_config = txt_config
        return TextBlock._default_style_config


class ImageBlock:
    _default_style_config : ImageConfig | None = None

    def __init__(self, image_url="", is_image_local=False, darken_image=True, image_config=None):
        self.content_image_url: str = image_url
        self.is_image_local : bool = is_image_local
        self.image_config : ImageConfig = ImageBlock.get_default_image_config(image_config)

    @staticmethod
    def get_default_image_config(config : ImageConfig | None):
        if config != None:
            return config
        if ImageBlock._default_style_config == None:
            img_config = ImageConfig.load_image_config_from_file('default_image_config.json')
            ImageBlock._default_style_config = img_config
        return ImageBlock._default_style_config


@dataclass
class Frame:
    # TODO: make this class contain a list of textual and image objects with each of them having their own configs
    textual_content : List[TextBlock] | None = None
    image_content : ImageBlock = ImageBlock()
    content_segmented : List[Frame] | None = None
    use_segmented : bool = False
    use_image: bool = False
