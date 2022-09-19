from __future__ import annotations

from dataclasses import dataclass
from typing import List

@dataclass
class Content:
    content : str = ""
    content_image_url: str = ""
    content_segmented : List[Content] | None = None
    use_segmented : bool = False
    use_image: bool = False
    is_image_local : bool = False
    darken_image : bool = True