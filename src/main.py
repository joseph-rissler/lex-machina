import sys

from config import config, init_config

if len(sys.argv) < 2 or sys.argv[1] == "bot":
    import bot, data
    init_config()
    bot.run()
elif sys.argv[1] == "test":
    import bot
    init_config('test')
    bot.run()
elif sys.arv[1] == "console":
    import code
    code.InteractiveConsole(locals=globals()).interact()
