from datetime import datetime

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from tabulate import tabulate

from constants import *
from localization.string_builder import make_month_title


def time_is_over(date_str: str) -> bool:
    date = datetime.strptime(date_str, DATE_FORMAT)
    current_date = datetime.now()
    return current_date >= date


def make_table(items, lang: str, record_click_callback=None, prefix='') -> list:
    data = list()
    for item in items:
        btn_id = item[KEY_ID]
        name = item[KEY_NAME]
        date = datetime.strptime(item[KEY_DATE], DATE_FORMAT).date()
        date_title = f'{make_month_title(date.month, lang)} {date.year}'
        title = f'{prefix}    {name}  {date_title}'
        record = Button(
            Const(title),
            id=str(btn_id),
            on_click=record_click_callback
        )
        data.append(record)
    return data

