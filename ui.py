from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo
from aiogram_dialog.widgets.kbd.button import WebApp

from config import WEBAPP_DOMAIN
from localization.string_builder import (
    make_add_btn_title,
    make_del_btn_title,
    make_actual_btn_title,
    make_expired_btn_title,
)


def make_main_menu(lang_code: str) -> ReplyKeyboardMarkup:
    btn_add = KeyboardButton(
        make_add_btn_title(lang_code),
        web_app=WebAppInfo(url=f'https://{WEBAPP_DOMAIN}/add_drug')
    )
    btn_del = KeyboardButton(make_del_btn_title(lang_code))
    btn_view_actual = KeyboardButton(make_actual_btn_title(lang_code))
    btn_view_expired = KeyboardButton(make_expired_btn_title(lang_code))
    btn_info = KeyboardButton('❓')

    main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu.add(btn_view_actual)
    main_menu.insert(btn_view_expired)
    main_menu.add(btn_add)
    main_menu.insert(btn_del)
    # main_menu.insert(btn_info)

    return main_menu
