from telebot.apihelper import ApiTelegramException
from ..utube import get_qualities, download
from .keyboard import qualities_keyboard, main_keyboard
from threading import Thread

__all__ = ["start", "get_link", "send_video", "get_resolution", "is_subscribed"]

def start(message, bot, texts):
	print("functions.py > start")
	try:
		bot.send_message(
			message.chat.id,
			texts["hello"].format(name = message.from_user.first_name + " " + message.from_user.last_name or ''),
			reply_markup = main_keyboard(texts)
		)
		return True, '', ''
	except Exception as err:
		return False, str(err), repr(err)

def get_link(message, bot, text):
	print("functions.py > get_link")
	try:
		bot.send_message(
			message.chat.id,
			text.format(url = message.text),
			reply_markup = qualities_keyboard(*get_qualities(message.text))
		)
		return True, '', ''
	except Exception as err:
		return False, str(err), repr(err)

def send_video(bot, url, chat_id, quality):
	print("functions.py > send_video")
	path = download(url, quality)
	bot.send_video(chat_id, open(path, 'rb'))

def get_resolution(message, bot, text, url):
	print("functions.py > get_resolution")
	try:
		bot.send_message(message.chat.id, text)
		t = Thread(lambda:send_video(bot, url, message.chat.id, message.text))
		t.start()
		return True, '', ''
	except Exception as err:
		return False, str(err), repr(err)

def is_subscribed(chat_id, user_id, bot):
	print("functions.py > is_subscribed")
	# from: https://stackoverflow.com/questions/64414486/how-to-check-if-a-user-is-subscribed-to-a-specific-telegram-channel-python-py
	try:
		bot.get_chat_member(chat_id, user_id)
		return True
	except ApiTelegramException as e:
		if e.result_json['description'] == 'Bad Request: user not found':
			return False
