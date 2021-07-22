from pytube import YouTube
import time
from urllib.error import HTTPError

def get_qualities(url):
	yt = YouTube(url)
	for wait in range(3):
		try:
			return {stream.resolution for stream in yt.streams.filter(type="video")}
		except HTTPError as err:
			if wait==2: raise err

def download(url,quality):
	yt = YouTube(url)
	for wait in range(3):
		try:
			return yt.streams.filter(res = quality).first().download()
		except HTTPError as err:
			if wait==2: raise err

def get_sizes(url):
	yt = YouTube(url)
	for wait in range(3):
		try:
			return {stream.resolution: stream.filesize for stream in yt.streams.filter(type="video")}
		except HTTPError as err:
			if wait==2: raise err

def get_size(url, quality):
	yt = YouTube(url)
	for wait in range(3):
		try:
			return yt.streams.filter(res = quality).first().filesize
		except HTTPError as err:
			if wait==2: raise err