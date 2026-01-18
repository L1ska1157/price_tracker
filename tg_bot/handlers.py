from aiogram.filters import (
    Command
    )
from aiogram.fsm.context import (
    FSMContext
)
from aiogram.types import (
    Message, 
    CallbackQuery,
    ReplyKeyboardRemove
    )
from aiogram import (
    F, 
    Router
    )
from tg_bot.states import (
    States
)
from database.func import (
    add_user,
    add_product,
    get_all,
    delete_product
)
from exceptions import (
    RecordAlreadyExistsError,
    BadResponse,
    WrongLink,
    NotProductPage
)
from parser import (
    parse,
    shops_list,
    get_graph
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
        shops_str += f'\n{shop.name.capitalize()}'
        
    await message.answer(
        text=f'Привіт! Цей бот створений для зручного відслідковування цін на товари. Підтримувані магазини: {shops_str}\nЩоб додати новий товар до відсслідковування, просто надішліть посилання на нього мені, і я скажу вам, коли його ціна зміниться',
        reply_markup=kb.menu_kb
    )
    
    
# ---- HELP func
@router.message(Command('help'))
async def help_command(message: Message):
    log.info(f'Command /help from user {message.chat.username}')
    add_user(
            user_id = message.chat.id
        )
    
    shops_str = ''
    for shop in shops_list:
        shops_str += f'\n{shop.name.capitalize()}'
        
    await message.answer(
        text=f'Цей бот створений для зручного відслідковування цін на товари. \nПідтримувані магазини: {shops_str}\nЩоб додати новий товар до відсслідковування, просто надішліть посилання на нього мені, і я скажу вам, коли його ціна зміниться. \nВикористайте клавіатуру знизу, щоб переглянути збережені товари, видалити товар який ви більше не хочете відслідковувати або переглянути графік зміни цін за останні 7 днів. \nВраховуйте, що у мене немає даних про ціну товару до того як ви його додали',
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
        
    except WrongLink:
        log.info('User gives unavaliable link')
        await message.answer(text='Це посилання недоступне \nНа жаль, зараз я не можу працювати з цим сайтом')
        
    except BadResponse as e:
        log.warning(f'Bad response \n{e}')
        await message.answer(text='Це посилання недоступне \nПеревірте його на правильність. Якщо посилання правильне, можливо сайт тимчасово не відповідає')

    except NotProductPage:
        log.warning('not a product page')
        await message.answer(text='Перевірте, чи ви надали посилання саме на товар')

    except RecordAlreadyExistsError:
        log.warning('Already existing product')
        await message.answer(text=f'Ви вже відслідковуєте цей товар! \nЙого ціна зараз {data['price']} грн')
        
    except Exception as e:
        log.error(f'Unexpected error: {e}')
        

# ---- Send all products saved by this user 
@router.message(Command('price_list')) # TODO
@router.message(F.text == 'Збережені товари')
async def f(message: Message):
    log.info(f'Command /price_list from user {message.chat.username}')
    products = get_all(
        user_id = message.chat.id
    )
    mes = 'Звісно! Ось збережені вами продукти: \n'
    for product in products:
        mes += f'> <a href="{product.link}">{product.name}</a>   {product.price_0} грн\n'
    await message.answer(mes, parse_mode='html')


# ---- Getting price graph - start. Switch status, give products list
@router.message(Command('get_graph'))
@router.message(F.text == 'Графік ціни')
async def get_graph_get_list(message: Message, state: FSMContext):
    log.info(f'Command /get_graph from user {message.chat.username}')
    products_list = get_all(
            user_id = message.chat.id
        )
    keyboard = await kb.inline_builder(
        product_list = products_list
    )
    remove_msg = await message.answer('⏳', reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text = 'Виберіть товар зі списку нижче, і я згенерую графік його ціни за останні 7 днів. Посилання поруч допоможуть не помилитися', 
        reply_markup = keyboard
    )
    await remove_msg.delete()
    await state.update_data(
        products = products_list
    )
    await state.set_state(States.get_graph)


# ---- Finally, getting price graph
@router.callback_query(States.get_graph)
async def get_graph_send_image(callback: CallbackQuery, state: FSMContext):
    log.info(f'Catched callback with data {callback.data} from user {callback.message.chat.username} while getting graph of product')
    
    if callback.data == 'return':
        await callback.message.answer(
            text = 'Повертаюсь',
            reply_markup = kb.menu_kb
        )
    else:
        data = await state.get_data()
        product = data['products'][int(callback.data)]
        img_link = get_graph(product)
        await callback.message.answer_photo(img_link, caption=product.name, reply_markup=kb.menu_kb)
        
    await callback.message.edit_reply_markup(reply_markup = None)
    await callback.answer()
    
    await state.clear()


# ---- Starting deleting process. Switch status to delete, send message
@router.message(Command('delete'))
@router.message(F.text == 'Видалити товар')
async def delete_product_get_list(message: Message, state: FSMContext):
    log.info(f'Command /delete from user {message.chat.username}')
    products_list = get_all(
            user_id = message.chat.id
        )
    keyboard = await kb.inline_builder(
        product_list = products_list
    )
    remove_msg = await message.answer('⏳', reply_markup=ReplyKeyboardRemove())
    await message.answer(
        text = 'Виберіть товар для видалення зі списку нижче. Посилання поруч допоможуть не помилитися', 
        reply_markup = keyboard
    )
    await remove_msg.delete()
    await state.update_data(
        products = products_list
    )
    await state.set_state(States.delete)
    

# ---- Finally, deleting choosen product from db or returning
@router.callback_query(States.delete)
async def delete_product_change_db(callback: CallbackQuery, state: FSMContext):
    log.info(f'Catched callback with data {callback.data} from user {callback.message.chat.username} while deleting product')
    
    if callback.data == 'return':
        await callback.message.answer(
            text = 'Повертаюсь',
            reply_markup = kb.menu_kb
        )
    else:
        data = await state.get_data()
        link = data['products'][int(callback.data)].link
        
        name = delete_product(
            user_id = callback.message.chat.id,
            link = link
            )
        await callback.message.answer(
            text = f'Товар {name} більше не відстежується',
            reply_markup = kb.menu_kb
        )
    await callback.message.edit_reply_markup(reply_markup = None)
    await callback.answer()
    
    await state.clear()
    
    
# ---- If user is trying to send smth when choosing product. To buttons don't stay
@router.message(States.get_graph)
@router.message(States.delete)
async def try_to_send_when_choosing_product(message: Message):
    log.info(f'Message when choosing from user {message.chat.username}')
    await message.answer(
        text = 'Будь ласка, оберіть товар зі списку вище або натисніть "Назад"'
    )
    
    
# ---- If user sends something out of bot functional
@router.message()
async def mes_reaction(message: Message):
    log.info(f'User {message.chat.username} send something that I don\'t know...')
    await message.answer_sticker('CAACAgIAAxkBAAEQRWxpbVa1zmYv-RYMFmEjMJQYPzqaqgACRRMAAjBLWUk_VuT9OAYobzgE')