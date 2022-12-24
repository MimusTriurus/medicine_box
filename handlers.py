import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton

from components import dp
from db_management import sql_get_drugs, sql_add_user, sql_add_drug, sql_del_drugs, sql_clear_expired_drugs
from helpers import make_table_str, validate_date, time_is_over
from localization.string_builder import *
from ui import make_main_menu, make_cancel_menu


class FSMAddDrug(StatesGroup):
    name = State()
    date = State()


class FSMDelDrug(StatesGroup):
    id = State()


@dp.message_handler(Text(equals=ru_strings[ID_START]))
async def request_start_handler(message: types.Message):
    lang = message.from_user.language_code
    await sql_add_user(message.from_user.id)
    await message.answer(
        make_start_message(lang),
        parse_mode=types.ParseMode.HTML,
        reply_markup=make_main_menu(lang)
    )


@dp.message_handler(Text(equals=make_add_btn_title(RU)))
async def request_add_drug_handler(message: types.Message, state=None):
    lang = message.from_user.language_code

    await FSMAddDrug.name.set()
    await message.reply(
        make_add_drug_name_message(lang),
        parse_mode=types.ParseMode.HTML,
        reply_markup=make_cancel_menu(lang)
    )


async def request_set_drug_name_handler(message: types.Message, state: FSMContext):
    lang = message.from_user.language_code
    if message.text == make_cancel_btn_title(lang):
        await message.reply(
            make_cancelled_message(lang),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )
        await state.finish()
        return

    async with state.proxy() as data:
        data['name'] = message.text
    await FSMAddDrug.next()
    await message.reply(
        make_add_drug_date_message(lang),
        parse_mode=types.ParseMode.HTML
    )


async def request_set_drug_date_handler(message: types.Message, state: FSMContext):
    lang = message.from_user.language_code
    if message.text == make_cancel_btn_title(lang):
        await message.reply(
            make_cancelled_message(lang),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )
        await state.finish()
        return

    if not validate_date(message.text):
        await message.reply(
            make_error_on_set_date_message(lang),
            parse_mode=types.ParseMode.HTML,
        )
    else:
        async with state.proxy() as data:
            drug_name = data['name']
            drug_date = message.text
            data['date'] = drug_date

        if time_is_over(message.text):
            await message.reply(
                make_drug_is_expired_message(lang, drug_name, drug_date),
                parse_mode=types.ParseMode.HTML,
                reply_markup=make_main_menu(lang)
            )
            await sql_add_drug(message.from_user.id, state, KEY_TABLE_AID_KIT_EXPIRED)
            await state.finish()
        else:
            await sql_add_drug(message.from_user.id, state)
            await state.finish()
            await message.reply(
                make_drug_added_message(lang, drug_name, drug_date),
                parse_mode=types.ParseMode.HTML,
                reply_markup=make_main_menu(lang)
            )


@dp.message_handler(Text(equals=make_del_btn_title(RU)))
async def request_del_drug_handler(message: types.Message, state=None):
    lang = message.from_user.language_code
    records = await sql_get_drugs(message.from_user.id)
    if records:
        await FSMDelDrug.id.set()
        table_string = make_table_str(records, True)
        await message.answer(
            make_4_del_drugs_table_message(lang, table_string),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_cancel_menu(lang)
        )
    else:
        await message.answer(
            make_first_aid_kit_is_empty_message(lang),
            parse_mode=types.ParseMode.HTML
        )


async def request_set_drug_id_4_del_handler(message: types.Message, state: FSMContext):
    lang = message.from_user.language_code
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


@dp.message_handler(Text(equals=make_actual_btn_title(RU)))
async def request_view_first_aid_kit(message: types.Message):
    lang = message.from_user.language_code
    records = await sql_get_drugs(message.from_user.id)
    if records:
        table_string = make_table_str(records)
        await message.answer(
            make_drugs_table_message(lang, table_string),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )
    else:
        await message.answer(
            make_first_aid_kit_is_empty_message(lang),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )


@dp.callback_query_handler(text=make_clean_btn_title(RU))
async def inline_kb_answer_callback_handler(query: types.CallbackQuery):
    lang = query.message.from_user.language_code
    await sql_clear_expired_drugs(query.from_user.id)
    await query.message.answer(make_done_message(lang))


@dp.message_handler(Text(equals=make_expired_btn_title(RU)))
async def request_view_first_aid_kit_expired(message: types.Message):
    lang = message.from_user.language_code

    keyboard_markup = types.InlineKeyboardMarkup()
    clean_btn = InlineKeyboardButton(make_clean_btn_title(lang), callback_data=make_clean_btn_title(lang))

    keyboard_markup.add(clean_btn)

    records = await sql_get_drugs(message.from_user.id, KEY_TABLE_AID_KIT_EXPIRED)
    if records:
        table_string = make_table_str(records)
        await message.answer(
            make_expired_drugs_table_message(lang, table_string),
            parse_mode=types.ParseMode.HTML,
            reply_markup=keyboard_markup
        )
    else:
        await message.answer(
            make_expired_drugs_lst_is_empty_message(lang),
            parse_mode=types.ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )
