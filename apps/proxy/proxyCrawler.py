import re

from tornado.gen import sleep
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
import datetime

from MagicPool.config import CRAWEL_INTERVAL_TIME, REDIS_PROXY_KEY
from utils.redisClient import RedisClient

from MagicPool.baseCrawler import BaseCrawler


class ProxyCrawler(BaseCrawler):
    _self = None

    def __init__(self, db):
        super().__init__()
        self._db = db

    @classmethod
    async def current(cls):
        if not cls._self:
            db = await RedisClient.current()
            cls._self = cls(db)

        return cls._self

    async def crawler_89ip(self, count=100, port=''):
        """
        异步生成器, 获取ip
        """
        url = "http://www.89ip.cn/tqdl.html?" \
            f"api=1&num={count}&port={port}&address=&isp="

        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url, headers=self.headers)
        if response.code == 200:
            for record in re.finditer(
                    "(\d+.\d+.\d+.\d+:\d+)",
                    str(response.body)
            ):
                yield record.group(0)
        else:
            print("crawler_89ip 匹配代理失败")

    async def run(self):

        while True:
            print(f"{datetime.datetime.now()}: 开始爬取代理ip")

            if await self._db.count(REDIS_PROXY_KEY) < 100:
                async for record in self.crawler_89ip():
                    await self._db.add(REDIS_PROXY_KEY, record)

            print(f"{datetime.datetime.now()}:爬取代理ip结束")
            await sleep(CRAWEL_INTERVAL_TIME)


if __name__ == '__main__':
    crawler = ProxyCrawler.current()
    IOLoop.current().run_sync(crawler.run)
