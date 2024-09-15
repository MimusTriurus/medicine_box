
from aiogram import types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from components import dp
from db_management import sql_add_user
from localization.string_builder import *


class FSMDelDrug(StatesGroup):
    id = State()


@dp.message_handler(Text(equals='/start'))
@dp.message_handler(Text(equals=localizers[EN].gettext(ID_START)))
@dp.message_handler(Text(equals=localizers[RU].gettext(ID_START)))
async def request_start_handler(message: types.Message):
    lang = message.from_user.language_code
    await sql_add_user(message.from_user.id, lang)
    photo = open('resources/images/botLogo.png', 'rb')
    await message.answer_photo(
        photo,
        caption=make_start_message(lang),
        parse_mode=types.ParseMode.HTML,
        # reply_markup=make_main_menu(lang, str(message.from_user.id))
    )
