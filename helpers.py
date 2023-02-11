from datetime import datetime

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.text import Const
from tabulate import tabulate

from constants import *


def time_is_over(date_str: str) -> bool:
    date = datetime.strptime(date_str, DATE_FORMAT)
    current_date = datetime.now()
    return current_date >= date


def make_table(items, record_click_callback=None, prefix='') -> list:
    data = list()
    for item in items:
        btn_id = item[KEY_ID]
        name = item[KEY_NAME]
        date = item[KEY_DATE]
        title = f'{prefix}    {name}  {date}'
        record = Button(
            Const(title),
            id=str(btn_id),
            on_click=record_click_callback
        )
        data.append(record)
    return data

