from database.database import (
    metadata,
    sync_engine,
    async_engine,
    async_ses_factory
)
from database.models import (
    Users,
    Products
)
from sqlalchemy import (
    insert
)
from config import (
    settings
)
import logging


# *** Functions for work with database


log = logging.getLogger(__name__)

# ---- Creates tables. Won't create if they exists
def create_tables():
    log.info('Creating tables')
    metadata.create_all(sync_engine)
    

# ---- Add new user if doesn't exists
async def add_user(user_id: int):
    async with async_ses_factory() as ses:
        log.info('Adding user')
        new_user = Users(id=user_id)
        await ses.merge(new_user)
        await ses.commit()
