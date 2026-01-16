from config import (
    settings
)
from aiogram import (
    Bot, 
    Dispatcher
)
from tg_bot.handlers import (
    router
)
from database.func import (
    create_tables
)
from custom import (
    set_custom_logging
)
import asyncio


# *** Startpoint        


bot = Bot(token=settings.BOT_TOKEN) 
dp = Dispatcher() 

async def main():
    create_tables()
    
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    set_custom_logging() # just some coloring for log messages
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('---- EXIT')