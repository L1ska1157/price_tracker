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
    create_tables,
    parse_all,
)
from logging_setup import (
    logging_setup
)
from apscheduler.schedulers.asyncio import (
    AsyncIOScheduler
)
from parser import (
    shops_list
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
    
    scheduler = AsyncIOScheduler()
    scheduler.add_job(
        parse_all, 
        trigger='cron', 
        hour='10,15,20', 
        minute=0, 
        kwargs={
            'bot': bot,
            'shop_list': shops_list
            } 
    )
    
    scheduler.start()  
    
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('[ EXIT ]')