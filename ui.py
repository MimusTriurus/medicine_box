from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from localization.string_builder import (
    get_strings_dict,
    make_add_btn_title,
    make_del_btn_title,
    make_actual_btn_title,
    make_expired_btn_title, make_cancel_btn_title
)


def make_main_menu(lang_code: str) -> ReplyKeyboardMarkup:
    btn_add = KeyboardButton(make_add_btn_title(lang_code))
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


def make_cancel_menu(lang_code: str) -> ReplyKeyboardMarkup:
    btn_cancel = KeyboardButton(make_cancel_btn_title(lang_code))

    main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
    main_menu.add(btn_cancel)

    return main_menu
