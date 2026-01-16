from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
    )
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder
    )


# *** Keyboards for tg bot


menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Видалити товар'),
            KeyboardButton(text='Збережені товари')
         ]
    ],
    resize_keyboard=True,
    
)

async def inline_builder(product_list: list[dict]):
    keyboard = InlineKeyboardBuilder() 
    for index in len(product_list):
        item = product_list[index]
        keyboard.add(
            InlineKeyboardButton(
                text=item['name'], 
                callback_data=index
                )
            ) 
        keyboard.add(
            InlineKeyboardButton(
                text='Переглянути',
                url=item['url']
            )
            )
    return keyboard.adjust(2).as_markup() 