from dataclasses import dataclass


@dataclass
class ContentProviderConfig:
    max_frames : int = 10