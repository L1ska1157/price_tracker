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


# *** Functions for work with database


# ---- Creates tables. Won't create if they exists
def create_tables():
    metadata.create_all(sync_engine)
    

# ---- Add new user if doesn't exists
async def add_user(user_id: int):
    async with async_ses_factory() as ses:
        new_user = Users(id=user_id)
        ses.merge(new_user)
        await ses.commit()
