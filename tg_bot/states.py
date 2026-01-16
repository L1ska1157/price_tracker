from aiogram.fsm.state import (
    StatesGroup, 
    State
)


# *** States for FSMContext in tgbot


class States(StatesGroup):
    delete = State()