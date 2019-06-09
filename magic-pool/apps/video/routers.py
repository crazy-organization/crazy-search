from apps.video.videoHandler import VideoHandler

video_routers = [("/video/(.*?)", VideoHandler)]