from telebot import types

__all__ = ["main_keyboard", "qualities_keyboard"]

def main_keyboard(texts):
	markup = types.ReplyKeyboardMarkup(row_width = 2)
	markup.add(
		types.KeyboardButton(texts["keyboard-main-learn"]),
		types.KeyboardButton(texts["keyboard-main-about"])
	)
	return markup

def qualities_keyboard(*qualities):
	markup = types.ReplyKeyboardMarkup(row_width = 3)
	markup.add(*(
		types.KeyboardButton(quality)
		for quality in qualities
	))
	return markup
