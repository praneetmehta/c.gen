from dataclasses import dataclass
import dataclasses
import json
from types import SimpleNamespace
from typing import List, Tuple

from config.util.containers import Pair, Triplet


@dataclass
class ImageConfig:
    resolution : Pair
    bg_color : Triplet
    image_url : str
    darken : bool = True

    @staticmethod
    def load_image_config_from_file(filename):
        img_config_json = open('config/{}'.format(filename), 'r').read()
        img_config : ImageConfig = json.loads(img_config_json, object_hook=lambda d: SimpleNamespace(**d))
        return img_config


    