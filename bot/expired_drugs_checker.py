import json
import logging
import os

from aiogram import Bot, types, Dispatcher
from aiogram.types import InlineKeyboardButton, WebAppInfo, InlineKeyboardMarkup
from pika.adapters.blocking_connection import BlockingChannel

from bot.config import WEBAPP_DOMAIN
from db_management import sql_check_expired_drugs, sql_get_lang

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from localization.string_builder import make_expired_drug_message

import pika

scheduler = AsyncIOScheduler()

log = logging.getLogger()


async def check_every_day(dispatcher: Dispatcher):
    log.info('check expired drugs...')
    expired_drugs = await sql_check_expired_drugs()
    for drug in expired_drugs:
        usr_id = int(drug[1])
        drug_name = drug[2]
        expired_date = drug[3]
        lang = await sql_get_lang(usr_id)

        inline_btn_info = InlineKeyboardButton(
            f'💊  Buy',
            web_app=WebAppInfo(url=f'https://google.com')
        )
        inline_kb = InlineKeyboardMarkup().add(inline_btn_info)
        message = make_expired_drug_message(lang, drug_name, expired_date)
        await dispatcher.bot.send_message(
            usr_id,
            message,
            parse_mode=types.ParseMode.HTML,
            reply_markup=inline_kb
        )


async def check_expired_drugs_queue(dispatcher: Dispatcher, queue_channel: BlockingChannel):
    if queue_channel:
        queue_name = os.getenv('RABBITMQ_QUEUE_NAME', default='medicine_box')
        r = queue_channel.basic_get(queue_name, True)
        if r and r[2]:
            drug = json.loads(r[2])

            usr_id = int(drug['user_id'])
            drug_name = drug['name']
            expired_date = drug['date']
            drug_id = drug['drug_id']

            lang = await sql_get_lang(usr_id)
            inline_btn_info = InlineKeyboardButton(
                f'₽  Buy',
                web_app=WebAppInfo(url=f'https://{WEBAPP_DOMAIN}/get_drug_stores?drug_id={drug_id}')
            )
            inline_kb = InlineKeyboardMarkup().add(inline_btn_info)
            message = make_expired_drug_message(lang, drug_name, expired_date)
            await dispatcher.bot.send_message(
                usr_id,
                message,
                parse_mode=types.ParseMode.HTML,
                reply_markup=inline_kb
            )
