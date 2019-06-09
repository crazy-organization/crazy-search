"""
    author: jim
    date: 2018-11-05

    测试代理ip.
"""
from tornado.gen import Multi, sleep
from tornado.httpclient import AsyncHTTPClient, HTTPError, HTTPRequest

from MagicPool.config import (TEST_COUNT, REDIS_PROXY_KEY,
                              TEST_INTERVAL_TIME, TEST_URL)
from utils.redisClient import RedisClient


class ProxyTester:

    _self = None

    def __init__(self, db):
        self._db = db

    @classmethod
    async def current(cls):
        if not cls._self:
            db = await RedisClient.current()
            cls._self = cls(db)

        return cls._self

    async def test_single_proxy(self, proxy):
        """
        测试单个proxy是否可用
        """
        if isinstance(proxy, bytes):
            proxy = str(proxy, 'utf-8')

        proxy_host, proxy_port = proxy.split(":")

        http_client = AsyncHTTPClient()
        http_request = HTTPRequest(
            url=TEST_URL,
            proxy_host=proxy_host,
            proxy_port=int(proxy_port)
        )

        try:
            response = await http_client.fetch(http_request)
            if response.code == 200:
                await self._db.max(REDIS_PROXY_KEY, proxy)
            else:
                await self._db.decrease(REDIS_PROXY_KEY, proxy)
        except HTTPError as e:
            # print(str(e))
            await self._db.decrease(REDIS_PROXY_KEY, proxy)

    async def run(self):
        while True:
            print("开始测试...")
            proxy_count = await self._db.count(REDIS_PROXY_KEY, 0, 100)
            for start in range(0, proxy_count, TEST_COUNT):
                end = min(start+TEST_COUNT, proxy_count)
                print(f"正在测试{start} - {end} 的代理")
                proxys = await self._db.range(REDIS_PROXY_KEY, start, end)
                await Multi(map(self.test_single_proxy, proxys))
                print(f"{start}-{end} 条代理已测完")

            print("测试结束...")
            await sleep(TEST_INTERVAL_TIME)


if __name__ == '__main__':
    pass
