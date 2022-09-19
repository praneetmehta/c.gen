from content_provider.config.content_provider_request import ContentProviderRequest
from content_provider.config.content_provider_type import ContentProviderType
from content_provider.config.default_content_provider_config import ContentProviderConfig

class ContentProviderRequestFactory:

    @staticmethod
    def get_request(type : ContentProviderType) -> ContentProviderRequest:
        if type == ContentProviderType.TCT:
            url = input("Enter the resource URL: \n >>> ")
            return ContentProviderRequest("", url)
        return ContentProviderRequest("")

    @staticmethod
    def get_request_config(type : ContentProviderType) -> ContentProviderConfig:
        if type == ContentProviderType.TCT:
            return ContentProviderConfig(15)
        return ContentProviderConfig()