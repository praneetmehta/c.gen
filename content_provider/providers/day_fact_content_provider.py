from datetime import date
from pydoc import text

from bs4 import BeautifulSoup
from config.util.decorators import overrides
from content_provider.config.content import Content
from content_provider.config.content_provider_request import ContentProviderRequest
from content_provider.config.default_content_provider_config import ContentProviderConfig
from content_provider.providers.content_provider import ContentProvider

import requests

class DayFactContentProvider(ContentProvider):
    @overrides(ContentProvider)
    def generate_content(self, request: ContentProviderRequest, config: ContentProviderConfig) -> Content:
        url : str = "https://www.thefactsite.com/day/{}-{}/".format(date.today().strftime("%B"), date.today().day)
        
        content : Content = self.scrape_facts_for_today(url, config.max_frames)
        return content

    def scrape_facts_for_today(self, url : str, max_frames : int) -> Content:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        cards = soup.find_all("article", class_="otd-event")
        content_list = list()
        content_list.append(Content(str(date.today().day) + "-" + date.today().strftime("%B") ))
        content_list.append(Content(" ", "resources/tih.jpeg", None, False, True, True, False))
        for card in cards[:max_frames]:
            tmp = card.find("h3").text
            imgs = card.find("img")
            if imgs != None:
                content_list.append(Content(tmp, imgs['data-src'], None, False, True, False))
            else:
                content_list.append(Content(tmp))
        content_list.append(Content("Follow for more!!"))
        return Content("","", content_list, True)

    