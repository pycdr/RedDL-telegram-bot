from telebot.apihelper import ApiTelegramException
from ..utube import get_qualities, download, get_sizes, get_size
from .keyboard import qualities_keyboard, main_keyboard
from threading import Thread
from os import remove
import traceback

def sizeof_fmt(num, suffix='B'):
    # https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
    for unit in ['','Ki','Mi','Gi','Ti','Pi','Ei','Zi']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)

def start(message, bot, texts):
	try:
		bot.send_message(
			message.chat.id,
			texts["hello"].format(name = (message.from_user.first_name or '') + " " + (message.from_user.last_name or '')),
			reply_markup = main_keyboard(texts)
		)
		return True, '', ''
	except Exception as err:
		return False, str(err), traceback.format_exc()

def get_link(message, bot, text, err429_text):
	try:
		bot.send_message(
			message.chat.id,
			"\n\n".join(f"{x}: {sizeof_fmt(y)}" for x,y in get_sizes(message.text).items())
		)
		bot.send_message(
			message.chat.id,
			text.format(url = message.text),
			reply_markup = qualities_keyboard(*get_qualities(message.text))
		)
		return True, '', ''
	except Exception as err:
		if getattr(err, 'code', None) == 429: err = err429_text
		return False, str(err), traceback.format_exc()

def send_video(bot, url, chat_id, quality):
	path = download(url, quality)
	file_id = (bot.send_video(chat_id, open(path, 'rb'))).video.file_id
	remove(path)
	return file_id

def get_resolution(message, bot, text, url, max_size, size_err_text, err429_text):
	try:
		if get_size(url, message.text) > max_size:
			bot.send_message(message.chat.id, size_err_text)
			return True, '', ''
		bot.send_message(message.chat.id, text)
		t = Thread(target = lambda:send_video(bot, url, message.chat.id, message.text))
		t.start()
		return True, '', ''
	except Exception as err:
		if getattr(err, 'code', None) == 429: err = err429_text
		return False, str(err), traceback.format_exc()

def is_subscribed(chat_id, user_id, bot):
	# from: https://stackoverflow.com/questions/64414486/how-to-check-if-a-user-is-subscribed-to-a-specific-telegram-channel-python-py
	try:
		res = bot.get_chat_member(chat_id, user_id)
		return True if res.status != 'left' else False
	except ApiTelegramException as e:
		if e.result_json['description'] == 'Bad Request: user not found':
			return False
		else:
			print(traceback.format_exc())
			raise e