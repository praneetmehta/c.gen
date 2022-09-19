from dataclasses import dataclass
import json
from types import SimpleNamespace
from config.util.containers import Pair, Triplet
from .font_enum import Font

@dataclass
class TextConfig:
    color: Triplet
    size: int
    offset_percent: Pair
    scale: float
    align: str
    font: Font
    split_by_lines: int

    @staticmethod
    def load_text_config_from_file(config_name):
        txt_config_json = open('config/{}'.format(config_name), 'r').read()
        txt_config : TextConfig = json.loads(txt_config_json, object_hook=lambda d: SimpleNamespace(**d))
        txt_config.font = Font.CHALK
        return txt_config