from apps.novel.novelHandler import NovelHandler

novel_routers=[("/novel/(.*?)", NovelHandler)]