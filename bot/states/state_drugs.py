from aiogram.dispatcher.filters.state import State, StatesGroup


class FSMViewDrugs(StatesGroup):
    drugs = State()


class FSMDelDrugs(StatesGroup):
    drugs = State()


class FSMExpiredDrugs(StatesGroup):
    drugs = State()
