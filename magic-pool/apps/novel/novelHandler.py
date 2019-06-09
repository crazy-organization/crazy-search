from apps.novel.crawler.novelCrawler_biqudu import NovelCrawler_biqudu

from MagicPool.baseHandler import BaseHandler


class NovelHandler(BaseHandler):

    async def get_browser(self):

        name = self.get_argument("name", None)
        if not name:
            return self.fail("请输入书名")
        norvelCrawler = NovelCrawler_biqudu()

        try:
            author, last_update_time, content = await norvelCrawler.crawl_biqudu_index(name)
        except Exception as e:
            return self.fail(str(e))

        return self.success({
            "author": author,
            "last_update_time": last_update_time,
            "content": content
        })

    async def get_content(self):

        url = self.get_argument("url", None)
        if not url:
            return self.fail("请输入url")

        norvelCrawler = NovelCrawler_biqudu()
        header, content = await norvelCrawler.crawl_biqudu_content(url)
        return self.success({"header": header, "content": content})

    async def get(self, method):
        return await eval("self."+method)()
