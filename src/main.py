import sys

from config import config, init_config

if len(sys.argv) < 2 or sys.argv[1] == "bot":
    init_config()
    import bot
    bot.run()
elif sys.argv[1] == "test":
    init_config('test')
    import bot
    bot.run()
elif sys.arv[1] == "console":
    import code
    code.InteractiveConsole(locals=globals()).interact()
