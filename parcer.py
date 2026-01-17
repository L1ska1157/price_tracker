from bs4 import (
    BeautifulSoup
)
import lxml
import requests
import logging 
from database.models import ShopType
import re


# *** Parcer


log = logging.getLogger(__name__)


def parce(shop: ShopType, link: str):
    headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-UA,ru;q=0.9,uk-UA;q=0.8,uk;q=0.7,ru-RU;q=0.6,en-US;q=0.5,en;q=0.4'
    }
    parcing_classes = shop.value
    if type(parcing_classes) == tuple:
        parcing_classes = parcing_classes[0]

    log.info(f'Getting price for product from {shop.name}')
    
    response = requests.get(url=link, headers=headers)

    soup = BeautifulSoup(response.content, features='lxml')
    with open('page.html', 'w', encoding='utf-8') as f:
        f.write(soup.prettify())
    price = int(
        re.sub(
            r'\D', 
            '', 
            soup.find(class_=parcing_classes['price']).get_text()
        )
    )
    # name = (
    #     soup.find
    # )
    
    log.info(f'Got price = {price}\nLink: {link}')
    return {
        # 'name': name,
        'price': price        
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
        print(f'{item["shop"].name}: ')
        print(parce(
            link = item['link'],
            shop = item['shop']
            ))