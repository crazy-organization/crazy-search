import asyncio
import aiohttp
from MagicPool.baseCrawler import BaseCrawler
from bs4 import BeautifulSoup


class NovelCrawler_biqudu(BaseCrawler):

    def __init__(self):
        self.base_url_biqudu = "https://www.biqudu.com"
        self.timeout = 30

    async def crawl_biqudu_index(self, name):
        """ 在笔趣阁中搜索小说得到目录url

        Args:
            name: 小说名

        Returns:
            novel_index: 小说目录首页页面的数据
            (作者, 最后更新时间, {小说章节名: 小说url, ....})

        Exceptions:
            超时
        """

        query_url = f"{self.base_url_biqudu}/searchbook.php"
        params = {
            "keyword": name
        }

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as client:
            resp = await client.get(query_url, params=params,
                                    headers=self.headers, ssl=False)
            resp_text = await resp.text()

            try:
                book_url = BeautifulSoup(resp_text, 'lxml').select(
                    "#hotcontent > div > div > div.image > a")[0]['href']
            except Exception:
                raise Exception("未搜索到该小说")

            resp = await client.get(self.base_url_biqudu + book_url,
                                    headers=self.headers, ssl=False)
            resp_text = await resp.text()

            soup = BeautifulSoup(resp_text, "lxml")

            # 小说info
            author = soup.select("#info p")[0].string
            last_update_time = soup.select("#info p")[2].string

            # 小说章节名和url
            book_section_a = soup.select("#list > dl > dd > a")
            content = dict()
            [content.update({_.string: _['href']}) for _ in book_section_a]

            return (author, last_update_time, content)

    async def crawl_biqudu_content(self, url):
        """ 根据url爬去biqudu的章节内容

            Args:
                url: 章节url

            Returns: (章节名, 章节内容)
        """

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as client:
            resp = await client.get(self.base_url_biqudu + url,
                                    headers=self.headers, ssl=False)

            resp_text = await resp.text()
            soup = BeautifulSoup(resp_text, 'lxml')

            # 小说章节名
            content_header = soup.select(".bookname")[0].h1.string

            # 文本内容
            content = soup.select("#content")[0]
            # 清除script标签
            [content.extract() for content in content('script')]

            return (content_header, content.text.lstrip().rstrip())


async def main():
    # novelCrawler = NovelCrawler_biqudu()
    # novel_index = await novelCrawler.crawl_biqudu_index("人皇纪")
    # print(novel_index)

    # novel_content = await novelCrawler.crawl_biqudu_content("/22_22509/2470305.html")
    # print(novel_content)

    novelCrawler = NovelCrawler_biqudu()
    await novelCrawler.crawl_index()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
