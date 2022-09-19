from config.util.decorators import overrides
from content_provider.config.frame import Frame, TextBlock
from content_provider.config.content_provider_request import ContentProviderRequest
from content_provider.config.default_content_provider_config import ContentProviderConfig
from content_provider.providers.content_provider import ContentProvider


class DummyContentProvider(ContentProvider):
    
    @overrides(ContentProvider)
    def generate_content(self, request: ContentProviderRequest, config: ContentProviderConfig) -> Frame:
        return Frame([TextBlock("This is a dummy content for {content}".format(content = request.request_topic))])