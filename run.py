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
from logging_setup import (
    logging_setup
)
import asyncio
import logging


# *** Startpoint        


bot = Bot(token=settings.BOT_TOKEN) 
dp = Dispatcher() 

async def main():
    logging_setup()
    log = logging.getLogger(__name__) 
    log.info('Running')
    
    create_tables()
    
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('[ EXIT ]')