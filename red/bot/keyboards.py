import telebot

class Keyboard:
	def generate(self):
		pass


class NormalKeyboard(Keyboard):
	def __init__(self, buttons=tuple()):
		"""@buttons: array of arrays of 'text'"""
		self.buttons = buttons

	def generate(self):
		if self.buttons is None or len(self.buttons) == 0:
			return telebot.types.ReplyKeyboardRemove()
		markup = telebot.types.ReplyKeyboardMarkup()
		for row in self.buttons:
			markup.add(*(
				telebot.types.KeyboardButton(text)
				for text in row
			))
		return markup


class InlineKeyboard(Keyboard):
	def __init__(self, buttons):
		"""@buttons: array of arrays of {'text': 'query'}"""
		self.buttons = buttons

	def generate(self):
		markup = telebot.types.InlineKeyboardMarkup()
		for row in self.buttons:
			markup.add(*(
				telebot.types.InlineKeyboardButton(text=data[0], callback_data=data[1])
				for data in row
			))
		return markup