import json

from tornado.web import RequestHandler


class BaseHandler(RequestHandler):

    def __init_(self):
        pass

    def success(self, data):
        """ 成功的相应请求

        """
        if isinstance(data, list):
            data = str(data)

        result = {
            "ret": 0,
            "data": data
        }

        self.write(json.dumps(result, ensure_ascii=False))
        return self.finish()

    def fail(self, msg):
        """ 失败的响应请求

        """
        result = {
            "ret": -1,
            "msg": msg
        }

        self.write(json.dumps(result, ensure_ascii=False))
        return self.finish()
