from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMAddDrug(StatesGroup):
    name = State()
    date = State()
