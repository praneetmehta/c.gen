from typing import List
from bs4 import BeautifulSoup
import requests
from datetime import date

from tqdm import tqdm
from config.util.decorators import overrides
from content_provider.config.frame import Frame, ImageBlock, TextBlock
from content_provider.config.content_provider_request import ContentProviderRequest
from content_provider.config.default_content_provider_config import ContentProviderConfig
from content_provider.providers.content_provider import ContentProvider
from image_generator.entities.text_config import TextConfig


class TheCrazyTouristContentProvider(ContentProvider):
    @overrides(ContentProvider)
    def generate_content(self, request: ContentProviderRequest, config: ContentProviderConfig) -> Frame:
        assert request.request_url != None, "Request url cannot be null for this content provider"
        content : Frame = self.scrape_facts_for_today(request.request_url, config.max_frames)
        return content

    def scrape_facts_for_today(self, url : str, max_frames : int) -> Frame:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        article_list = soup.find_all("div", class_="inside-article")
        content_list : List[Frame] = list()
        # content_list.append(Content((' ').join(url.split('.com')[1].strip('/').split('-'))))
        if article_list != None and len(article_list) > 0:
            article = article_list[0]
            content_list.append(Frame([TextBlock(article.find("h1").text)]))
        #     header = article.find_all("h2", recursive=False)[0].text
        #     condensed_list = article.find_all("ul", recursive=False)[0]
        #     for li in condensed_list.find_all("li"):
        #         content_list.append(Content(li.text))

        entry_content = soup.find_all("div", class_="entry-content")
        if entry_content != None and len(entry_content) > 0:
            h2s = entry_content[0].find_all("h2")
            figs = entry_content[0].find_all("figure")
            for i, h2 in tqdm(enumerate(h2s)):
                try:
                    img = figs[i].find("img")['src']
                    subtitle_text = figs[i].find("img").findNext("p")
                    content_list.append(Frame([TextBlock(h2.text, \
                        TextConfig.load_text_config_from_file('left_title_text_config.json')),
                        TextBlock(subtitle_text.text, \
                        TextConfig.load_text_config_from_file('left_subtitle_text_config.json'))], \
                        ImageBlock(img), None, False, True))
                except Exception as e:
                    print(e)
                    content_list.append(Frame([TextBlock(h2.text)]))
        
        content_list.append(Frame([TextBlock("Follow for more!!", TextConfig.load_text_config_from_file("center_focus_big.json"))]))
        return Frame(content_segmented=content_list, use_segmented=True)