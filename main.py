from modules.bot import Bot
import json

config = json.load(open("config.json", "r"))
bot = Bot(**config)
bot.start()
