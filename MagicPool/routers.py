from apps.proxy.routers import proxy_routers
from apps.video.routers import video_routers
from apps.novel.routers import novel_routers

__all__ = ['routers']

# routers = [
#     (r"/proxy/(.*)", ProxyHandler),
#     (r"/video/(.*)", VideoHandler),
#     (r"/novel/(.*)", NovelHandler),
# ]

routers = []

routers += proxy_routers
routers += video_routers
routers += novel_routers