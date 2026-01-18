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
    select,
    delete
)
from sqlalchemy.exc import (
    IntegrityError
)
from config import (
    settings
)
from aiogram import (
    Bot
)
from parser import (
    parse
)
import datetime
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
            raise RecordAlreadyExistsError() # In headers => sending message that this product already tracking
        
        except Exception as e:
            log.error(f'Unknown error: {e}')


# ---- Move prices on 1 day
def move_price():
    log.info('Moving price')
    with ses_factory() as ses:
        query = (
            select(Products)
        )
        products = ses.execute(query).scalars().all()
        for product in products:
            product.price_6 = product.price_5
            product.price_5 = product.price_4
            product.price_4 = product.price_3
            product.price_3 = product.price_2
            product.price_2 = product.price_1
            product.price_1 = product.price_0
        ses.commit()
            
        
# ---- Parse all prices, if first parse in day - move prices
async def parse_all(shop_list: list, bot: Bot | None = None):
    if datetime.datetime.now().time() < datetime.time(15): # if it's first iteration today
        move_price()
        
    with ses_factory() as ses:
        query = (
            select(Products)
        )
        products = ses.execute(query).scalars().all()
        links_query = (
            select(Products.link, Products.price_0)
        )

        links = ses.execute(links_query).unique().all()
        updated_prices = {}
        for link in links:
            result = parse(link[0], shop_list)
            if result['price'] != link[1]:
                updated_prices[link[0]] = {
                    'price': result['price'],
                    'less_then_was': ((result['price'] - link[1]) < 0)
                    }
            
        for product in products:
            if product.link in updated_prices.keys():
                if updated_prices[product.link]['less_then_was']:
                    await bot.send_message(
                        chat_id = product.user_id,
                        text=f'У {product.name} знизилася ціна до {updated_prices[product.link]['price']} грн!\nПосилання на товар; {product.link}'
                    )
                else:
                    await bot.send_message(
                        chat_id = product.user_id,
                        text=f'На жаль, у {product.name} виросла ціна до {updated_prices[product.link]['price']} грн(\nПосилання на товар; {product.link}'
                    )
                product.price_0 = updated_prices[product.link]['price']
        
        ses.commit()
        
        
# ---- Gives all products, saved by this user
def get_all(user_id: int):
    log.info(f'Getting all products, saved by user with id {user_id}')
    with ses_factory() as ses:
        query = (
            select(Products)
            .filter_by(user_id = user_id)
        )
        products = ses.execute(query).scalars().all()
        return products
     
        
# ---- Delete item from db
def delete_product(user_id: int, link: str):
    with ses_factory() as ses:
        obj_to_delete = ses.get(Products, (user_id, link))
        log.info(f'Deleting object {obj_to_delete}')
        
        name = obj_to_delete.name
        
        ses.delete(obj_to_delete)
        ses.commit()
        
        return name