# MagicPool
目前有以下功能。
- 代理池。

- 迅雷账号池。暂未完成。

- 视频池。 暂仅支持腾讯连续剧。

- 小说池。

 
## 接口  (请善良对待它们)
### 代理ip
获取代理ip
<br>
www.wenfengboy.com/proxy/gain    
<br>
代理ip池的数量
<br>
www.wenfengboy.com/proxy/count

### 视频
获取视频解析接口
<br>
www.wenfengboy.com/video/get_video_interface
<br>

获取视频url
<br>
www.wenfengboy.com/video/get_video_url_list?video_name=

### 小说
获取小说的章节链接
<br>
www.wenfengboy.com/novel/get_browser?name=
<br>
<br>
获取小说具体章节的标题及内容
<br>
www.wenfengboy.com/novel/get_content?url=

## 开发环境
python3.6以上

### 使用的第三方库
**tornado**
本项目中使用tornado的异步网络框架，提高网络的访问效率。
使用tornado的web框架当api接口。

**aioredis**
使用异步的redis提高对redis读取的效率。

**aiohttp**
使用异步的方式访问网络资源。


## 目录
- api
使用tornado web 完成请求接口s
- config
项目配置
- crwler
爬虫
- tester
测试
- utils
工具
- data
本地数据
- script
脚本存放路径


## 数据格式说明
### 小说json格式说明。
header: 小说章节名
<br>
content: 小说具体内容


## 日志
### 2019-01-01.

已完成对小说的url链接的获取，和具体章节内容的获取。

 Todo: 
 1. 切换小说源。 目前使用的是单一源， 如果该源出现问题，可以切换源，提高稳定性。
 2. 写脚本，将小说下载到本地数据库中，提高访问速度。