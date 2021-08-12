import telebot
from .components import Component


class Sender:
	def __init__(self, bot: telebot.TeleBot, t_id: int, reply: int = None):
		self.bot = bot
		self.t_id = t_id
		self.reply = reply

	def reply(self, reply: int = None):
		return Sender(self.bot, self.t_id, reply)

	def send(self, component: Component):
		return component.render(
			self.bot,
			chat_id=self.t_id,
			reply_to_message_id=self.reply
		)

	def __lshift__(self, component: Component):
		return self.send(component)


class Bot:
	"""
main class for working with telegram bot:
```
bot = red.bot.Bot('TOKEN')
bot.to(USER_OR_CHAT_ID).send(component)
(bot @ USER_OR_CHAT_ID).send(component)
bot @ USER_OR_CHAT_ID << component
```
	"""

	def __init__(self, token: str, cache=None) -> None:
		self.bot = telebot.TeleBot(token)
		self.cache = cache

	def set_cache(self, cache):
		self.cache = cache

	def to(self, t_id: int) -> Sender:
		return Sender(self.bot, t_id)

	def __matmul__(self, t_id: int) -> Sender:
		return self.to(t_id)

	def handler(self, typeof, values, function):
		assert typeof in ("command", 'query', 'regex', 'msgtype', 'filter'), \
			"<typeof> argument must be 'command', 'query', 'regex', 'msgtype' or 'filter'"
		assert isinstance(values, (list, tuple, set, frozenset)
		                  ), "<values> argument must be iterable."
		assert callable(function), "<function> argumnt must be callable."

		if typeof == "command":
			commands = [(command[1:] if command.startswith('/') else command) for command in values]
			@self.bot.message_handler(commands=commands)
			def handler(message):
				return function(
					messsage=message,
					cache=self.cache
				)
		elif typeof == "regex":
			for regex in values:
				@self.bot.message_handler(regexp=regex)
				def handler(message):
					return function(
						message=message,
						cache=self.cache
					)
		
		elif typeof == "msgtype":
			@self.bot.message_handler(content_types=values)
			def handler(message):
				return function(
					message=message,
					cache=self.cache
				)
		
		elif typeof == "filter":
			@self.bot.message_handler(
				func=lambda message: any(f(message) for f in values)
			)
			def handler(message):
				return function(
					message=message,
					cache=self.cache
				)
		
		elif typeof == "query":
			@self.bot.callback_query_handler(
				func=lambda message: any(f(message) for f in values)
			)
			def handler(query):
				return function(
					query=query,
					cache=self.cache
				)

	def __rshift__(self, values) -> None:
		assert isinstance(values, (list, tuple, set, frozenset)) and len(values) == 3, \
			"(Bot >> 'typeof', 'value'|['values',...], function) is only available, and with tuple."
		return self.hanlder(*values)
