from modules.bot import Bot
import json

try:
    config = json.load(open("config.json", "r"))
    bot = Bot(**config)
    print("main.py > bot.start()")
    bot.start()
except Exception as err:
	try:
		for debugger_id in bot.debuggers_id:
			if debugger_id not in bot.chat_ids: continue
			bot.bot.send_message(
				bot.chat_ids[debugger_id],
				f"bad and unfixable error is catchen! details: {debug_msg}"
			)
	except Exception as bad_err:
		print(f"not able to send error to admins!\ndetails of main error: {repr(err)}\nnew error: {repr(bad_err)}")