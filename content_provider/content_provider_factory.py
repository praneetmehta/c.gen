from typing import Dict
from content_provider.providers.content_provider import ContentProvider
from content_provider.config.content_provider_type import ContentProviderType
import logging

from content_provider.exceptions.content_provider_not_found import ContentProviderNotFoundException
from content_provider.providers.dummy_content_provider import DummyContentProvider
from content_provider.providers.day_fact_content_provider import DayFactContentProvider
log = logging.getLogger(__name__)

class ContentProviderFactory:
    """ Your application needs to have a instance of content provider factory and register the providers through the provided method"""
    _content_providers : Dict[ContentProviderType, ContentProvider]

    def __init__(self):
        self._content_providers = {}
        self._register_content_provider(ContentProviderType.DUMMY, DummyContentProvider())
        self._register_content_provider(ContentProviderType.DAY_FACT, DayFactContentProvider())

    def _register_content_provider(self, type : ContentProviderType, provider : ContentProvider) -> None:
        if type in self._content_providers:
            log.warn("Not registering provider of type {} as it is already registered".format(type))
            return
        self._content_providers[type] = provider

    def get_content_provider(self, type : ContentProviderType) -> ContentProvider | None:
        if type in self._content_providers:
            return self._content_providers.get(type)
        raise ContentProviderNotFoundException("Requested content provider of type {} not found".format(type))