#main.py

import handlers.user_handlers
import handlers.mod_handlers
import database
import config
from aiogram import Bot, Dispatcher
import asyncio

async def main():
    bot  = Bot(token = config.BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(handlers.mod_handlers.router)
    dp.include_router(handlers.user_handlers.router)


    await dp.start_polling(bot)

if __name__ == '__main__':
    print("Bot started")
    database.init_db()
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Бот остановлен")
    except Exception as error:
        print(error)

