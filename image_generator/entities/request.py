from dataclasses import dataclass

from content_provider.config.content import Content


@dataclass
class Request:
    content: Content
    output_path: str
