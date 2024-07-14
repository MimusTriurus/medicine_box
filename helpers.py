from datetime import datetime

from aiogram_dialog.widgets.kbd import Button
from aiogram_dialog.widgets.kbd.button import WebApp
from aiogram_dialog.widgets.text import Const
from flask import request

from constants import *
from localization.string_builder import make_month_title

import socket
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
external_ip = s.getsockname()[0]
s.close()


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
        if len(item) == 5:
            drug_id = item[4]
            record = WebApp(Const(title), url=Const(f'https://{external_ip}:8000/get_drug_info?{KEY_DRUG_ID}={drug_id}'))

        data.append(record)
    return data

