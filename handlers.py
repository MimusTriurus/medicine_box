import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager, StartMode
from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const, Jinja

from components import dp
from db_management import sql_get_drugs, sql_add_user, sql_del_drugs, sql_set_lang
from dialogs.view_drugs_dialog import view_actual_drugs_table, del_actual_drugs_table, expired_drugs_table
from helpers import make_table
from localization.string_builder import *
from states.state_add_drug import FSMAddDrug
from states.state_drugs import FSMViewDrugs, FSMDelDrugs, FSMExpiredDrugs
from ui import make_main_menu


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
        reply_markup=make_main_menu(lang)
    )


@dp.message_handler(Text(equals=make_add_btn_title(EN)))
@dp.message_handler(Text(equals=make_add_btn_title(RU)))
async def request_add_drug_handler(message: types.Message, dialog_manager: DialogManager, state=None):
    lang = message.from_user.language_code
    await sql_set_lang(message.from_user.id, lang)
    start_data = {LANG: lang}
    await dialog_manager.start(FSMAddDrug.name, mode=StartMode.RESET_STACK, data=start_data)


@dp.message_handler(Text(equals=make_del_btn_title(EN)))
@dp.message_handler(Text(equals=make_del_btn_title(RU)))
async def request_del_drug_handler(message: types.Message, dialog_manager: DialogManager):
    lang = message.from_user.language_code
    await sql_set_lang(message.from_user.id, lang)
    records = await sql_get_drugs(message.from_user.id)
    if records:
        del_actual_drugs_table.buttons = make_table(
            records,
            lang,
            del_actual_drug_from_db,
            ICON_CROSS_MARK
        )
        start_data = {LANG: lang}
        await dialog_manager.start(FSMDelDrugs.drugs, mode=StartMode.RESET_STACK, data=start_data)
        dialog_manager.current_context().dialog_data[LANG] = lang
    else:
        await message.answer(
            make_first_aid_kit_is_empty_message(lang),
            parse_mode=types.ParseMode.HTML
        )


async def request_set_drug_id_4_del_handler(message: types.Message, state: FSMContext):
    lang = message.from_user.language_code
    await sql_set_lang(message.from_user.id, lang)
    if message.text == make_cancel_btn_title(lang):
        await message.reply(
            make_cancelled_message(lang),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )
        await state.finish()
        return

    drugs_id = message.text.split(' ')
    deleted_drugs = list()
    not_found_drugs = list()
    for drug_id in drugs_id:
        if re.match('[0-9]+', drug_id):
            deleted_drug = await sql_del_drugs(int(drug_id))
            if deleted_drug:
                deleted_drugs.append(deleted_drug)
            else:
                not_found_drugs.append(drug_id)
    if deleted_drugs:
        reply_message = ''
        for drug in deleted_drugs:
            reply_message += f'{make_drug_deleted_message(lang, drug[0], drug[1])}\n'
        await state.finish()
        await message.reply(
            reply_message,
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )
    else:
        await message.reply(
            make_drug_not_found_message(lang, ' '.join(not_found_drugs)),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )


async def go_clicked(c: CallbackQuery, button: Button, manager: DialogManager):
    await c.message.answer("<b>123</b>123", parse_mode="HTML")


async def del_actual_drug_from_db(c: CallbackQuery, button: Button, manager: DialogManager):
    db_drug_id = button.widget_id
    if db_drug_id:
        deleted_drug = await sql_del_drugs(int(db_drug_id))
        if deleted_drug:
            lang = manager.current_context().dialog_data[LANG]
            button.text = Const(make_drug_deleted_message(lang, deleted_drug[0]))


async def del_expired_drug_from_db(c: CallbackQuery, button: Button, manager: DialogManager):
    db_drug_id = button.widget_id
    if db_drug_id:
        deleted_drug = await sql_del_drugs(int(db_drug_id), KEY_TABLE_AID_KIT_EXPIRED)
        if deleted_drug:
            button.text = Const(make_drug_deleted_message(c.from_user.language_code, deleted_drug[0]))


@dp.message_handler(Text(equals=make_actual_btn_title(EN)))
@dp.message_handler(Text(equals=make_actual_btn_title(RU)))
async def request_view_first_aid_kit(message: types.Message, dialog_manager: DialogManager):
    lang = message.from_user.language_code
    await sql_set_lang(message.from_user.id, lang)
    records = await sql_get_drugs(message.from_user.id)
    if records:
        view_actual_drugs_table.buttons = make_table(
            records,
            lang,
            None,
            # ICON_INFO
        )
        start_data = {LANG: lang}
        await dialog_manager.start(FSMViewDrugs.drugs, mode=StartMode.RESET_STACK, data=start_data)
    else:
        await message.answer(
            make_first_aid_kit_is_empty_message(lang),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )


@dp.message_handler(Text(equals=make_expired_btn_title(EN)))
@dp.message_handler(Text(equals=make_expired_btn_title(RU)))
async def request_view_first_aid_kit_expired(message: types.Message, dialog_manager: DialogManager):
    lang = message.from_user.language_code
    await sql_set_lang(message.from_user.id, lang)
    records = await sql_get_drugs(message.from_user.id, KEY_TABLE_AID_KIT_EXPIRED)
    if records:
        expired_drugs_table.buttons = make_table(
            records,
            lang,
            del_expired_drug_from_db,
            ICON_CROSS_MARK
        )
        start_data = {LANG: lang}
        await dialog_manager.start(FSMExpiredDrugs.drugs, mode=StartMode.RESET_STACK, data=start_data)
    else:
        await message.answer(
            make_expired_drugs_lst_is_empty_message(lang),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )


# @dp.message_handler(content_types="web_app_data")  # получаем отправленные данные
@dp.message_handler(content_types=types.message.ContentTypes.WEB_APP_DATA)
def answer(webAppMes):
    print(webAppMes)  # вся информация о сообщении
    print(webAppMes.web_app_data.data)  # конкретно то что мы передали в бота
