from apps.proxy.proxyHandler import ProxyHandler
proxy_routers = [
    ("/proxy/(.*?)", ProxyHandler),
]