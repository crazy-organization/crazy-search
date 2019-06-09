class BaseCrawler:

    def __init__(self):
        pass

    @property
    def headers(self):
        return {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64)"
            " AppleWebKit/537.36 (KHTML, like Gecko)"
            " Chrome/70.0.3538.77 Safari/537.36",
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
        }

    @property
    def retry_max_num(self):
        """ 超时重试次数

        """
        return 3
