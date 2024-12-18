import json
import logging
import os

from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardButton, WebAppInfo, InlineKeyboardMarkup
from pika.adapters.blocking_connection import BlockingChannel

from constants import (
    KEY_LANG,
    RU,
    KEY_USER_ID,
    KEY_NAME,
    KEY_DATE,
    KEY_DRUG_ID,
    KEY_TABLE_AID_KIT_EXPIRED,
    EMPTY_DRUG_ID
)
from config import WEBAPP_DOMAIN

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from localization.string_builder import make_expired_drug_message, make_buy_drug_btn_title

scheduler = AsyncIOScheduler()

log = logging.getLogger()


async def check_expired_drugs_queue(dispatcher: Dispatcher, queue_channel: BlockingChannel):
    if queue_channel:
        queue_name = os.getenv('RABBITMQ_QUEUE_NAME', default='medicine_box')
        r = queue_channel.basic_get(queue_name, True)
        if r and r[2]:
            expired_drugs = json.loads(r[2])
            for drug in expired_drugs[KEY_TABLE_AID_KIT_EXPIRED]:
                usr_id = int(drug[KEY_USER_ID])
                drug_name = drug[KEY_NAME]
                expired_date = drug[KEY_DATE]
                lang = drug.get(KEY_LANG, RU)
                inline_kb = InlineKeyboardMarkup()
                if KEY_DRUG_ID in drug:
                    drug_id = drug[KEY_DRUG_ID]
                    if drug_id != EMPTY_DRUG_ID:
                        inline_btn_info = InlineKeyboardButton(
                            f'🛒 {make_buy_drug_btn_title(lang)}',
                            web_app=WebAppInfo(url=f'https://{WEBAPP_DOMAIN}/get_drug_stores?drug_id={drug_id}')
                        )
                        inline_kb.add(inline_btn_info)
                message = make_expired_drug_message(lang, drug_name, expired_date)
                await dispatcher.bot.send_message(
                    usr_id,
                    message,
                    parse_mode=types.ParseMode.HTML,
                    reply_markup=inline_kb
                )
