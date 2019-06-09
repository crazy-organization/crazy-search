import hashlib


class SecretUtils:

    def __init__(self):
        pass

    @staticmethod
    def md5(src):
        return hashlib.md5(bytes(src, "utf-8")).hexdigest()
