from aiogram.filters import (
    CommandStart, Command
    )
from aiogram.fsm.context import (
    FSMContext
)
from aiogram.types import (
    Message, CallbackQuery
    )
from aiogram import (
    F, Router
    )
from tg_bot.states import (
    States
)
from database.func import (
    add_user,
    add_product
)
from database.database import (
    RecordAlreadyExistsError
)
from parser import (
    parse,
    shops_list
)
import tg_bot.keyboards as kb
import logging


# *** User messages processing


router = Router()
log = logging.getLogger(__name__)

# ---- Start. Send hello message, add new user in db if not exists
@router.message(Command('start'))
async def start(message: Message):
    log.info(f'Command /start from user {message.chat.username}')
    add_user(
            user_id = message.chat.id
        )
    
    shops_str = ''
    for shop in shops_list:
        shops_str += f'\n{shop.name.capitalize}'
        
    await message.answer(
        text=f'Привіт! Цей бот створений для зручного відслідковування цін на товари. Підтримувані магазини: {shops_str}',
        reply_markup=kb.menu_kb
    )
    

# ---- If user send link. Send curent price, add to db if everything ok, else send message about some problem
@router.message(F.text.regexp(r'^https?://'))
async def new_prod(message: Message):
    log.info(f'Link got from user {message.chat.username}')
    
    try:
        data = parse(
            link = message.text.strip(),
            shops_list=shops_list
            )
        add_product(
            user_id=message.chat.id, 
            link = message.text.strip(),
            price = data['price'],
            name = data['name']
            )
        await message.answer(text=f'{data['name']} тепер відслідковується! \nЙого ціна зараз: {data['price']}')
        
    except ValueError as e:
        log.info('User gives unavaliable link')
        
        if e == 'Bad response':
            await message.answer(text='Це посилання недоступне \nПеревірте його на правильність. Якщо посилання правильне, можливо сайт тимчасово не відповідає')
        if e == 'Domain not mapped':
            await message.answer(text='Це посилання недоступне \nНа жаль, зараз я не можу працювати з цим сайтом')
            
    except RecordAlreadyExistsError:
        await message.answer(text=f'Ви вже відслідковуєте цей товар! \nЙого ціна зараз {data['price']} грн')
        
    except Exception as e:
        log.error(f'Unexpected error: {e}')
        

# ---- Starting deleting process. Switch status to delete, send message
@router.message(Command('delete') | F.text == 'Видалити товар')
async def delete_product(message: Message, state: FSMContext):
    log.info(f'Command /delete from user {message.chat.username}')
    await message.answer('Виберіть товар для видалення зі списку нижче. Посилання поруч допоможуть не помилитися')
    await state.set_state(States.delete)


# ---- Send all products saved by this user
@router.message(Command('price_list') | F.text == 'Збережені товари')
async def f(message: Message):
    log.info(f'Command /price_list from user {message.chat.username}')
    pass


# ---- If user is trying to send smth when deleting product. To not to deletion buttons
@router.message(States.delete)
async def try_to_send_whe_delete(message: Message, state: FSMContext):
    log.info(f'Message when deleting from user {message.chat.username}')
    await message.answer(
        text = 'Будь ласка, оберіть товар для видалення зі списку вище або натисніть "Назад"'
    )