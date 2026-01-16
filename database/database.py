from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from config import settings


# *** Database preferences


# ---- Engines
sync_engine = create_engine(
    url=settings.DATABASE_URL
)
async_engine = create_async_engine( 
    url = settings.DATABASE_URL_async()
)

# ---- Session factories
sync_ses_factory = sessionmaker(sync_engine)
async_ses_factory = async_sessionmaker(async_engine)

# ---- Models base
class Base(DeclarativeBase):
    pass

metadata = Base.metadata