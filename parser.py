from bs4 import (
    BeautifulSoup
)
from urllib.parse import (
    urlparse
) 
from exceptions import (
    BadResponse,
    WrongLink,
    NotProductPage
)
import lxml
import requests
import logging
import re
import datetime


# *** Parser and avaliable shops


log = logging.getLogger(__name__)


class Shop():
    def __init__(self, 
                 name: str, 
                 domain: str, 
                 name_class: str, 
                 price_class: str
                ):
        self.name = name
        self.domain = domain
        self.name_class = name_class
        self.price_class = price_class


shops_list = [ # Avaliable shops
        Shop(
            name = 'foxtrot',
            domain = 'foxtrot',
            name_class = 'page__title',
            price_class = 'product-box__main_price'
        ),
        Shop(
            name = 'comfy',
            domain = 'comfy',
            name_class = 'product-title',
            price_class = 'price__current'
        ),
        Shop(
            name = 'allo',
            domain = 'allo',
            name_class = 'p-view__header-title',
            price_class = 'a-product-price__current'
        ),
        Shop(
            name = 'cytrus',
            domain = 'ctrs',
            name_class = 'DescriptionTitle_title__PxMkv',
            price_class = 'price'
        ),
        Shop(
            name = 'moyo',
            domain = 'moyo',
            name_class = 'product_name',
            price_class = 'product_price_current'
        ),
        Shop(
            name = 'stylus',
            domain = 'stls',
            name_class = 'sc-4bec5e00-0',
            price_class = 'sc-7d638165-4'
        )
    ]


def get_shop(link: str, shops_list: list):
    domain = urlparse(link).netloc.lower() 
    
    for shop in shops_list:
        if shop.domain in domain:
            return shop
    
    return None



def parse(link: str, shops_list: list):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Linux; Android 13; Pixel 7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'Referer': 'https://www.google.com/'
    }
    
    # Get shop
    shop = get_shop(link, shops_list)
    if shop == None:
        raise WrongLink()
    log.info(f'Parsing data for product from {shop.name}')
    
    # Parse data
    response = requests.get(url=link, headers=headers)
    if response.status_code != 200:
        raise BadResponse() # processing in headers
    
    soup = BeautifulSoup(response.content, features='lxml')
    
    try:
        name = (
            soup.find(class_=shop.name_class).get_text().strip()
        )
        price = int(
            re.sub(
                r'\D', 
                '', 
                soup.find(class_=shop.price_class).get_text()
            )
        )
    except TypeError:
        raise NotProductPage()
    except Exception as e:
        log.error(f'Unexpected error: \n{e}')
    
    res = {
        'name': name,
        'price': price
    }
    
    log.info(f'Got price = {price}')
    return res


# ---- Getting price changes graph
def get_graph(product):
    log.info(f'Getting graph for product {product}')
    from quickchart import QuickChart

    qc = QuickChart() # object that gives link for image by given data
    qc.width = 1000
    qc.height = 600
    
    dates = []
    for i in range(6, -1, -1):
        dates.append(str(datetime.date.today() - datetime.timedelta(i)))
        
    prices = [product.price_6, product.price_5, product.price_4, product.price_3, product.price_2, product.price_1, product.price_0]
    
    qc.config = { 
        "type": "line",
        "data": {
            "labels": dates,
            "datasets": [{
                "label": "Prices",
                "data": prices
            }]
        },
        "options": {
            "legend": {
                "display": False
            }
        }
    }
    return qc.get_url()