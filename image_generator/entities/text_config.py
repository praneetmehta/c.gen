from dataclasses import dataclass
from config.util.containers import Pair, Triplet
from content_provider.config.content import Content
from .font_enum import Font

@dataclass
class TextConfig:
    color: Triplet
    size: int
    offset_percent: Pair
    scale: float
    align: str
    font: Font