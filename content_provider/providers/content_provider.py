from content_provider.config.content import Content
from content_provider.config.content_provider_request import ContentProviderRequest
from content_provider.config.default_content_provider_config import ContentProviderConfig


class ContentProvider:
    
    def generate_content(self, request : ContentProviderRequest, config : ContentProviderConfig) -> Content:
        return Content("EMPTY")