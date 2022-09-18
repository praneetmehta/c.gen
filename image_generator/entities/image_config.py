from dataclasses import dataclass
import dataclasses
from typing import List, Tuple

from config.util.containers import Pair, Triplet


@dataclass
class ImageConfig:
    resolution : Pair
    bg_color : Triplet
    image_url : str


    