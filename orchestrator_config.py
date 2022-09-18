from dataclasses import dataclass
from image_generator.entities.image_config import ImageConfig
from image_generator.entities.text_config import TextConfig
from content_provider.config.content_provider_type import ContentProviderType

@dataclass
class OrchestrationRequest:
    request_topic : str
    run_id: float
    image_config : ImageConfig
    text_config : TextConfig
    content_provider_type : ContentProviderType = ContentProviderType.DUMMY
    is_test : bool = True
    