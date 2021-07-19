from pytube import YouTube
import time

def get_qualities(url):
	yt = YouTube(url)
	return {stream.resolution for stream in yt.streams.filter(type="video")}

def download(url,quality):
	yt = YouTube(url)
	return yt.streams.filter(res = quality).first().download()
