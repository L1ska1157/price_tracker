from bs4 import (
    BeautifulSoup
)
import lxml
import aiohttp
import asyncio
import logging 
from database.models import ShopType


# *** Parcer


log = logging.getLogger(__name__)


async def parce(shop: ShopType, link: str):
    log.info(f'Getting price for product from {shop.value}')
    
    div_classes = {
        'foxtrot': {
            'price': 'product-box__main_price',
            'name': 
            },
        'comfy': 'price__current',
        'allo': 'a-product-price__current-price',
        'cytrus': 'price medium no-wrap f-secondary Price_price__KKCnw',
        'moyo': 'product_price_current',
        'stylus': 'sc-79f6e9d1-6 jaaakJ'
    }
    
    async with aiohttp.ClientSession() as ses:
        response = await ses.get(url=link)
    
    soup = BeautifulSoup(await response.text, 'lxml')
    price = int(
        soup.find(class_=div_classes[shop.value]['price'])
        .get_text()
        .replace(' ', '')
        .replace('₴', '')
        .replace('грн', '')
        )
    name = (
        soup.find
    )
    
    log.info(f'Got price = {price}\nLink: {link}')
    return {
        'price': price,
        'name': name
    }


if __name__ == '__main__':
    items_test = [
        {
            'link': 'https://www.foxtrot.com.ua/uk/shop/naushniki-sony-over-ear-wireless-mic-silver-wh1000xm6se.html',
            'shop': ShopType.foxtrot
        },
        {
            'link': 'https://comfy.ua/ua/navushniki-povnorozmirni-bezdrotovi-sony-wh-1000xm6-platinum-silver-wh1000xm6s-e.html?gad_source=1&gad_campaignid=20830332909&gclid=CjwKCAiA4KfLBhB0EiwAUY7GAT_xhds91Z3TqU0sf8UCTTtBrGVDbTTqijWpjw3p_zXC_2LiDpuVYxoCpz8QAvD_BwE',
            'shop': ShopType.comfy
        },
        {
            'link': 'https://allo.ua/ua/naushniki/naushniki-sony-wh-1000xm6-wh1000xm6s-e-silver.html?utm_source=google&utm_medium=cpc&utm_campaign=%21%5BP%5D_%7C_%5BPMax%5D_%7C_regular_%7C_%D0%A2%D0%B5%D0%BB%D0%B5%D0%BA%D0%BE%D0%BC_%7C_%D0%9D%D0%B0%D1%83%D1%88%D0%BD%D0%B8%D0%BA%D0%B8&gad_source=1&gad_campaignid=19542756862&gclid=CjwKCAiA4KfLBhB0EiwAUY7GAaTQFk5S9JL7j0eS3E-MHTnpFGK15jLd16ulOPyjUkX4fw3RY_BP4RoCcf8QAvD_BwE',
            'shop': ShopType.allo
        },
        {
            'link': 'https://www.ctrs.com.ua/naushniki/naushniki-sony-wh-1000xm6-silver-772847.html?gad_source=1&gad_campaignid=23012613511&gclid=CjwKCAiA4KfLBhB0EiwAUY7GAdNXyd7ZsTvUidXWb02Hll1euW15Ra-54weaEB99idzhLYK0enKWHRoCoxIQAvD_BwE',
            'shop': ShopType.cytrus
        },
        {
            'link': 'https://www.moyo.ua/ua/naushniki_sony_wh-1000xm6_silver_wh1000xm6s_e_/655653.html?utm_source=google&utm_medium=cpc&utm_id=22938363746&utm_id=22938363746&utm_campaign=Performance_Max_margin_20&gad_source=1&gad_campaignid=22938373142&gclid=CjwKCAiA4KfLBhB0EiwAUY7GAfjnLtz-8mJOpPm1L87cpqrcu4OCCDsiYUjD8O4fpxsqy02htwAsjBoCSeEQAvD_BwE',
            'shop': ShopType.moyo
        },
        {
            'link': 'https://stls.store/uk/sony-wh-1000xm6-platinum-silver-p1438143c102.html?utm_source=google&utm_medium=cpc&utm_campaign=allshop&gad_source=1&gad_campaignid=17999472874&gclid=CjwKCAiA4KfLBhB0EiwAUY7GAasI4WLMFWjEupeslyly56i_oMpyyP4O8ycWTonybBexGG0NPWwoxxoCpfAQAvD_BwE',
            'shop': ShopType.stylus
        }
    ]
    for item in items_test:
        print(parce(
            link = item['link'],
            shop = item['shop']
            ))