from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
    )
from aiogram.utils.keyboard import (
    InlineKeyboardBuilder
    )
import logging


# *** Keyboards for tg bot


menu_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Графік ціни')
        ],
        [
            KeyboardButton(text='Видалити товар'),
            KeyboardButton(text='Збережені товари')
         ]
    ],
    resize_keyboard=True,
    
)

async def inline_builder(product_list: list):
    log = logging.Logger(__name__)
    log.info(f'Making inline keybord with {len(product_list)} rows')
    
    keyboard = InlineKeyboardBuilder() 
    for index in range(len(product_list)):
        item = product_list[index]
        keyboard.add(
            InlineKeyboardButton(
                text=item.name, 
                callback_data=str(index)
                )
            ) 
        keyboard.add(
            InlineKeyboardButton(
                text='Переглянути',
                url=item.link
            )
            )
    keyboard.add(
        InlineKeyboardButton(
            text = 'Назад',
            callback_data = 'return'
        )
    )
    return keyboard.adjust(2).as_markup() 