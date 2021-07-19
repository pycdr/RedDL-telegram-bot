from modules.bot import Bot
import json

config = json.load(open("config.json", "r"))
bot = Bot(**config)
print("main.py > bot.start()")
bot.start()
