import asyncio
from random import choice

import aioredis

from MagicPool.config import REDIS_IP, REDIS_PORT


class RedisClient:

    _self = None

    def __init__(self, conn):
        """
        conn: redis连接
        """
        self._conn = conn

    @classmethod
    async def current(cls, redis_ip=REDIS_IP, reids_port=REDIS_PORT, **kwargs):
        """
        __init__ 不能设为异步,
        所以没办法初始化异步的aioredis, 所以在current中初始化aioredis
        """
        if not cls._self:
            conn = await aioredis.create_redis(
                f'redis://{redis_ip}:{reids_port}'
            )
            cls._self = cls(conn)

        return cls._self

    async def add(self, key, value):
        await self._conn.zadd(key, 90, value)

    async def decrease(self, key, value):
        """
        减少item分数，若小于等于0，则删除.
        """
        await self._conn.zincrby(key, -10, value)
        if await self.score(key, value) <= 0:
            await self.delItem(key, value)

    async def delItem(self, key, value):
        """
        删除指定项
        """
        await self._conn.zrem(key, value)

    async def max(self, key, value):
        """
        将该项设为满分
        """
        await self._conn.zadd(key, 100, value)

    async def range(self, key, start, stop):
        """
        分数由高到低的返回指定条数数据
        """
        return await self._conn.zrevrange(key, start, stop)

    async def count(self, key, start=100, stop=100):
        """
        获取在指定分数范围之内key的数量, 默认查找可用项的数量
        """
        return await self._conn.zcount(key, start, stop)

    async def score(self, key, value):
        """
        查看指定value的分数
        """
        return await self._conn.zscore(key, value)

    async def get(self, key):
        """
        得到一个可用的item
        """
        count = await self.count(key)
        if count:
            return str(choice(await self._conn.zrangebyscore(key, 100, 100)), "utf-8")
        else:
            return str(choice(await self.range(key, 0, 100)), "utf-8")


async def main():
    redis_client = await RedisClient.current()
    # await redis_client.add("name", "lisi")
    # await redis_client.decrease("xunlei", "{'username':'99715', 'password':'2l8J3e1'}")
    # await redis_client.increase("name", "lisi")
    # await redis_client.delLowScore("name")
    rst = await redis_client.range("xunlei", 0, 100)
    # rst = await redis_client.get("proxy")

    print(rst)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
