from MagicPool.baseCrawler import BaseCrawler
import aiohttp
from bs4 import BeautifulSoup

class NovelCrawler_biquge(BaseCrawler):

    def __init__(self):
        self.base_url = "https://www.biquge.com/"

    async def crawl_index(self, ):
        """
        :return:
        """
        async with aiohttp.ClientSession() as session:
            resp = await session.get(self.base_url, ssl=False)
            body = await resp.text()

            soup = BeautifulSoup(body, "lxml")
            # for nav_list in soup.select(".nav ul li")
