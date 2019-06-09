from MagicPool.config import REDIS_PROXY_KEY
from utils.redisClient import RedisClient
from MagicPool.baseHandler import BaseHandler


class ProxyHandler(BaseHandler):

    async def gain(self):
        redis_client = await RedisClient.current()
        return await redis_client.get(REDIS_PROXY_KEY)

    async def count(self):
        redis_client = await RedisClient.current()
        return str(await redis_client.count(REDIS_PROXY_KEY))

    async def get(self, method):
        result = await eval("self."+method)()
        return self.write(result)
