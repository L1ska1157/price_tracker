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
    add_user
)
import tg_bot.keyboards as kb
import validators
import logging


# *** User messages processing


router = Router()
log = logging.getLogger(__name__)

# ---- Start. Send hello message, add new user in db if not exists
@router.message(Command('start'))
async def start(message: Message):
    log.info(f'Command /start from user {message.chat.username}')
    await add_user(
            user_id = message.chat.id
        )
    # TODO МАГАЗИНИ!!!
    await message.answer(
        text='Привіт! Цей бот створений для зручного відслідковування цін на товари. Підтримувані магазини: [avaliable_shops]',
        reply_markup=kb.menu_kb
    )
    

# ---- If user send link. Check if this shop is avaliable, check if this product isn't in db from this user, else add it to db, if link is avaliable send actual price to user and message about adding product/that product already added
@router.message(validators.url(F.text))
async def new_prod(message: Message):
    log.info(f'[INFO] Link got from user {message.chat.username}')
    pass



# ---- Starting deleting ptocces. Switch status to delete, send message
@router.message(Command('delete') | F.text == 'Видалити товар')
async def delete_product(message: Message, state: FSMContext):
    log.info(f'[INFO] Command /delete from user {message.chat.username}')
    await message.answer('Виберіть товар для видалення зі списку нижче. Посилання поруч допоможуть не помилитися')
    await state.set_state(States.delete)


# ---- Send all products saved by this user
@router.message(Command('price_list') | F.text == 'Збережені товари')
async def f(message: Message):
    log.info(f'[INFO] Command /price_list from user {message.chat.username}')
    pass



# ---- If user is trying to send smth when deleting product. To not to deletion buttons
@router.message(States.delete)
async def try_to_send_whe_delete(message: Message, state: FSMContext):
    log.info(f'[INFO] Message when deleting from user {message.chat.username}')
    await message.answer(
        text = 'Будь ласка, оберіть товар для видалення зі списку вище або натисніть "Назад"'
    )