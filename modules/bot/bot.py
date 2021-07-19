from telebot import TeleBot
from time import ctime
from threading import Timer
from .functions import *

class Bot:
	def __init__(self, **data):
		self.bot = TeleBot(data["token"])
		self.bot.get_updates() # removes recieved messages!
		self.texts = data["texts"]
		self.admins_id = data["admins"]
		self.debuggers_id = data["debuggers"]
		self.channels_id = data["channels_id"]
		self.chat_ids = {}
		self.is_joined = {}
		self.checker = Timer(60, self.check_joins)
		self.sent_link = {}

	def check_joins(self):
		for x in self.is_joined:
			if self.is_joined[x]:
				self.is_joined[x] = all(is_subscribed(channel_id, x, self.bot) for channel_id in self.channels_id)

	def check_is_joined(self, message) -> bool:
		if not self.is_joined.get(message.from_user.id, False): # not joined or not available!
			self.is_joined[message.from_user.id] = all(is_subscribed(channel_id, message.from_user.id, self.bot) for channel_id in self.channels_id)
		if not self.is_joined[message.from_user.id]:
			self.bot.reply_to(
				message,
				self.texts["not-joined-yet"]
			)
		print(self.is_joined)
		return self.is_joined[message.from_user.id]

	def catch_err(self, message, user_msg, debug_msg):
		self.bot.reply_to(
			message,
			self.texts["user_message"].format(user_msg = user_msg)
		)
		if debug_msg:
			for debugger_id in self.debuggers_id:
				if debugger_id not in self.chat_ids: continue
				self.bot.send_message(
					self.chat_ids[debugger_id],
					f"error details at {ctime()} for message {message.text} from {message.from_user.first_name} {message.from_user.last_name or ''} @{message.from_user.username or ''} ({message.from_user.id}): \n{debug_msg}"
				)

	def init(self):
		@self.bot.message_handler(commands = ['start'])
		def cmd_start(message):
			if not self.check_is_joined(message): return
			successful, user_msg, debug_msg = start(message, self.bot, self.texts)
			if not successful:
				self.catch_err(message, user_msg, debug_msg)
			self.chat_ids[message.from_user.id] = message.chat.id

		@self.bot.message_handler(regexp = r'((http|https)://)?(www.)?(youtube.com|youtu.be)/(watch\?v=)?[a-zA-z0-9-_&=]+')
		def cmd_get_link(message):
			if not self.check_is_joined(message): return
			successful, user_msg, debug_msg = get_link(message, self.bot, self.texts["get-quality"])
			if not successful:
				self.catch_err(message, user_msg, debug_msg)
			else:
				self.sent_link[message.from_user.id] = message.text

		@self.bot.message_handler(regexp = r'[0-9]{3,4}p')
		def cmd_get_resolution(message):
			if message.from_user.id not in self.sent_link:
				self.bot.reply_to(
					message,
					self.texts["no-link-here"]
				)
				return
			successful, user_msg, debug_msg = get_resolution(message, self.bot, self.texts["uploading"], self.sent_link[message.from_user.id])
			if not successful:
				self.catch_err(message, user_msg, debug_msg)

	def start(self):
		self.init()
		self.checker.start()
		self.bot.polling()

