from datetime import date
from pydoc import text

from bs4 import BeautifulSoup
from config.util.decorators import overrides
from content_provider.config.frame import Frame, ImageBlock, TextBlock
from content_provider.config.content_provider_request import ContentProviderRequest
from content_provider.config.default_content_provider_config import ContentProviderConfig
from content_provider.providers.content_provider import ContentProvider

import requests

class DayFactContentProvider(ContentProvider):
    @overrides(ContentProvider)
    def generate_content(self, request: ContentProviderRequest, config: ContentProviderConfig) -> Frame:
        url : str = "https://www.thefactsite.com/day/{}-{}/".format(date.today().strftime("%B"), date.today().day)
        
        content : Frame = self.scrape_facts_for_today(url, config.max_frames)
        return content

    def scrape_facts_for_today(self, url : str, max_frames : int) -> Frame:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        cards = soup.find_all("article", class_="otd-event")
        content_list = list()
        content_list.append(Frame([TextBlock(str(date.today().day) + "-" + date.today().strftime("%B"))]))
        # content_list.append(Frame(" ", "resources/tih.jpeg", None, False, True, True, False))
        content_list.append(Frame([], ImageBlock("resources/tih.jpeg", True), None, False, True))
        for card in cards[:max_frames]:
            tmp = card.find("h3").text.split()
            tmp = (' ').join(tmp[0:1]).strip() + '\n\n' + (' ').join(tmp[1:]).strip()
            imgs = card.find("img")
            if imgs != None:
                content_list.append(Frame([TextBlock(tmp)], ImageBlock(imgs['data-src']), None, False, True))
            else:
                content_list.append(Frame([TextBlock(tmp)]))
        content_list.append(Frame([TextBlock("Follow for more!!")]))
        return Frame(content_segmented=content_list, use_segmented=True)

    