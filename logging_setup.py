import logging
import sys
from config import settings


# *** Logging preferences for better understending what happens (I don't like usual aiogram logging)


def logging_setup():
    level = logging.INFO if settings.LOGGING else logging.CRITICAL
    
    log_format = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    
    logging.basicConfig(
        level=level,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    
    logging.getLogger("aiogram").setLevel(logging.WARNING)