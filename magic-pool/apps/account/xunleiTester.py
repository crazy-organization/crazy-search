import json

import aiohttp
from tornado.ioloop import IOLoop

from utils.redisClient import RedisClient
from utils.secretUtils import SecretUtils
from feng_libs.data import ProxyPool

class XunLeiTester:

    _self = None

    def __init__(self, db):
        self._db = db

    @classmethod
    async def current(cls):
        if not cls._self:
            db = await RedisClient.current()
            cls._self = cls(db)

        return cls._self

    def encode_multipart_formdata(self, fields):
        boundary = '----WebKitFormBoundaryLKanADu8CiqolsSP'

        l = []
        crlf = '\r\n'

        for key, value in fields.items():
            l.append('--' + boundary)
            l.append('Content-Disposition: form-data; name="%s"' % key)
            l.append('')
            l.append(value)

        l.append('--' + boundary + '--')
        l.append('')
        body = crlf.join(l)
        content_type = 'multipart/form-data; boundary=%s' % boundary
        return content_type, body

    async def test_single_account(self, account):

        if isinstance(account, bytes):
            account = str(account, 'utf-8')

        account_json = json.loads(account)
        username = account_json['username']
        password = account_json['password']

        # username = '17688549537'
        # password = 'qaz642012137'
        # username = "18379150048"
        # password = "qaz642012137"
        # username = "ten123789"
        # password = "6420121"
        # username = "18814664597"
        # password = "libin18814664597"

        # 代理
        proxy = await ProxyPool.get_proxy()
        # proxy = None

        params = {
            'appid': '22003',
            'appName': 'WEB-i.xunlei.com',
            'deviceModel': 'chrome/70.0.3538.77',
            'deviceName': 'PC-Chrome',
            'OSVersion': 'Linux x86_64',
            'provideNname': 'NONE',
            'netWorkType': 'NONE',
            'providerName': 'NONE',
            'sdkVersion': 'v3.5.0',
            'clientVersion': '1.1.1',
            'protocolVersion': '301',
            'devicesign': 'wdi10.0ae86ea19ff457567ceb4b707cc0c0ff44e8bc57e630ebdf7efa1a5b92b1bb1f',    # 固定设备信息
            'platformVersion': '1',
            'fromPlatformVersion': '1',
            'format': 'cookie',
            # 'timestamp': '1542182400516',
            'userName': username,
            'passWord': password,
            'isMd5Pwd': '0',
            # 'creditkey': 'ck0.I8wdaBo1tx0TtyB5kbpHVsT6ncgkgyVnJmbAxk0w-abZX6A-48svawbqu9vyQtCMwmIRpH-JKeybMwbyYTSuZg'  # 可以不存在
        }

        content_type, body = self.encode_multipart_formdata(params)

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
            'Content-Type': content_type,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            # 'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Content-Length': '2251',
            'Upgrade-Insecure-Requests': '1',
        }

        self.headers2 = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.84 Safari/537.36',
        }

        data = aiohttp.FormData()
        data.add_field('file', body, content_type=content_type)
        try:
            async with aiohttp.ClientSession() as client:

                # login
                url = 'https://login.xunlei.com/xluser.core.login/v3/login'
                async with client.post(url, data=data, headers=self.headers, 
                                       proxy=proxy, timeout=30) as rsp:
                    # print(rsp.status)
                    # print(rsp.cookies)
                    deviceid = rsp.cookies['deviceid'].value[0:32]

                csrf_token = SecretUtils.md5(deviceid)

                # getAc15615428418Info
                # print("-"*40)
                url = "15615428418ttps://xluser-ssl.xunlei.com/xlcenter/v1/GetAccInfo?" \
                    f"csrf_token={csrf_token}"

                async with client.get(url, headers=self.headers2,
                                      proxy=proxy, timeout=30) as rsp:
                    print(rsp.status)
                    acc_info = await rsp.json()
                    print(acc_info)

                # getVipInfo
                # print("-"*40)
                vip_url = "https://xluser-ssl.xunlei.com/xlcenter/v1/" \
                    "GetAllVipInfo?" \
                    f"csrf_token={csrf_token}"
                # print([{cookie.key: cookie.value}
                #        for cookie in client.cookie_jar])

                async with client.get(vip_url, headers=self.headers2, 
                                      proxy=proxy, timeout=30) as rsp:
                    vip_info = await rsp.json()
                    print(vip_info)

        except Exception as e:
            print(str(e))
            return (1, account)

        # 判断账号是否可用
        if vip_info.get('code', 0) == 200:
            print("成功")
            return (0, account)
        else:
            return (1, account)

    async def run(self):
        print("开始测试...")

        rst = []

        await self.test_single_account('{"username":"18379150048", "password":"qaz642012137"}')

        # 检测
        # xunlei_count = await self._db.count(REDIS_XUNLEI_KEY, 0, 100)
        # for start in range(0, xunlei_count, TEST_COUNT):
        #     end = min(start+TEST_COUNT, xunlei_count)
        #     print(f"正在测试{start} - {end} 的迅雷账号")
        #     accounts = await self._db.range(REDIS_XUNLEI_KEY, start, end)
        #     rst += await Multi(map(self.test_single_account, accounts))
        #     print(f"{start}-{end} 条迅雷账号已测完")

        # # redis
        # for index, account in rst:
        #     if index == 0:
        #         await self._db.max(REDIS_XUNLEI_KEY, account)
        #     else:
        #         await self._db.decrease(REDIS_XUNLEI_KEY, account)
        print("测试结束...")


async def main():
    xunlei = await XunLeiTester.current()
    await xunlei.run()

if __name__ == '__main__':
    IOLoop.current().run_sync(main)
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(main())
