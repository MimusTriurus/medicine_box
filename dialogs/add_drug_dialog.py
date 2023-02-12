from datetime import date

from aiogram.types import Message, CallbackQuery, ParseMode
from aiogram_dialog import Dialog, Window, DialogManager
from aiogram_dialog.manager.protocols import ManagedDialogAdapterProto
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Cancel

from constants import KEY_DATE, KEY_NAME, KEY_TABLE_AID_KIT_EXPIRED, DATE_FORMAT
from db_management import sql_add_drug
from localization.string_builder import (
    make_drug_is_expired_message,
    make_drug_added_message,
    make_add_drug_name_message,
    make_add_drug_date_message,
    make_cancel_btn_title, make_month_title
)
from states.state_add_drug import FSMAddDrug
from ui import make_main_menu
from widgets.expiration_calendar import ExpirationCalendar
from widgets.localized_text import LocalizedText


async def get_data(dialog_manager: DialogManager, **kwargs):
    expired_date = dialog_manager.current_context().dialog_data.get(KEY_DATE, None)
    drug_name = dialog_manager.current_context().dialog_data.get(KEY_NAME, '')
    return {
        KEY_NAME: drug_name,
        KEY_DATE: expired_date
    }


async def on_drug_name_added(
        m: Message,
        dialog: ManagedDialogAdapterProto,
        manager: DialogManager
):
    if manager.is_preview():
        await dialog.next()
        return
    manager.current_context().dialog_data[KEY_NAME] = m.text
    await dialog.next()


async def on_expired_date_selected(
        c: CallbackQuery,
        widget,
        manager:
        DialogManager,
        selected_date: date
):
    mess = c.message
    lang = c.from_user.language_code
    dd = manager.current_context().dialog_data
    drug_name = dd[KEY_NAME]
    dd[KEY_DATE] = selected_date.strftime(DATE_FORMAT)
    date_title = f'{make_month_title(selected_date.month, lang)} {selected_date.year}'
    user_id = mess.chat.id
    current_date = date.today()
    if current_date > selected_date:
        await sql_add_drug(user_id, dd, KEY_TABLE_AID_KIT_EXPIRED)
        await mess.reply(
            make_drug_is_expired_message(lang, drug_name, date_title),
            parse_mode=ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )
    else:
        await sql_add_drug(user_id, dd)
        await mess.reply(
            make_drug_added_message(lang, drug_name, date_title),
            parse_mode=ParseMode.HTML,
            reply_markup=make_main_menu(lang)
        )
    await manager.done()

exp_calendar = ExpirationCalendar(
    id='expiration_calendar',
    on_click=on_expired_date_selected
)

add_drug_dialog = Dialog(
    Window(
        LocalizedText(make_add_drug_name_message),
        Cancel(text=LocalizedText(make_cancel_btn_title)),
        MessageInput(on_drug_name_added),
        state=FSMAddDrug.name
    ),
    Window(
        LocalizedText(make_add_drug_date_message),
        exp_calendar,
        Cancel(text=LocalizedText(make_cancel_btn_title)),
        state=FSMAddDrug.date,
        getter=get_data
    )
)
