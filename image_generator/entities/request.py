from dataclasses import dataclass

from content_provider.config.frame import Frame


@dataclass
class Request:
    content: Frame
    output_path: str
