from sqlalchemy import create_engine, String
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from config import settings


# *** Database preferences


# ---- Engines
engine = create_engine(
    url=settings.DATABASE_URL
)

# ---- Session factories
ses_factory = sessionmaker(engine)

# ---- Models base
class Base(DeclarativeBase):
    pass

metadata = Base.metadata
