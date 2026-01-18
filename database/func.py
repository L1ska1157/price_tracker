from database.database import (
    metadata,
    engine,
    ses_factory,
    RecordAlreadyExistsError
)
from database.models import (
    Users,
    Products
)
from sqlalchemy import (
    insert,
    select,
    and_
)
from sqlalchemy.exc import (
    IntegrityError
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
    metadata.create_all(engine)
    

# ---- Add new user if doesn't exists
def add_user(user_id: int):
    with ses_factory() as ses:
        log.info('Adding user')
        new_user = Users(id=user_id)
        ses.merge(new_user)
        ses.commit()
        
        
# ---- Add new product
def add_product(user_id: int, link: str, price: int, name: str):
    log.info('Adding product')
    with ses_factory() as ses:
        new_product = Products(
            user_id = user_id,
            link = link,
            price_0 = price,
            name = name
        )
        ses.add(new_product)
        try: 
            ses.commit()
            
        except IntegrityError:
            ses.rollback() 
            log.info('Trying to add existing link')
            raise RecordAlreadyExistsError('Link already tracking') # In headers => sending message that this product already tracking
        
        except Exception as e:
            log.error(f'Unknown error: {e}')


# ---- Move prices on 1 day
def move_price(user_id: int, link: str, today_price: int):
    log.info('Moving price')
    with ses_factory() as ses:
        query = (
            ses.select(Products)
            .filter(and_(
                Products.user_id == user_id,
                Products.link == link         
                ))
        )
        product = ses.execute(query).scalars().one()
        
        product.price_6 = product.price_5
        product.price_5 = product.price_4
        product.price_4 = product.price_3
        product.price_3 = product.price_2
        product.price_2 = product.price_1
        product.price_1 = product.price_0
        product.price_0 = today_price
            
        
# ---- Parse all prices, if first parse in day - move prices
