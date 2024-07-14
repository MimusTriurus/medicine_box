import logging
import os

from aiogram import Dispatcher
from aiogram.utils import executor
from aiogram.utils.executor import start_polling
from aiogram_dialog import DialogRegistry
from jinja2 import Template
from werkzeug import serving
import ssl

from db_management import sql_start, sql_stop
from drugs_db_management import (
    sql_drugs_db_connect,
    sql_get_drug_info_by_id,
    sql_drugs_db_stop,
    KEY_URL,
    KEY_TITLE,
    KEY_DESC,
    KEY_CONTRA,
    KEY_GROUP
)
from dialogs.add_drug_dialog import add_drug_dialog
from dialogs.view_drugs_dialog import view_actual_drugs_dialog, del_actual_drugs_dialog, view_expired_drugs_dialog
from expired_drugs_checker import scheduler, check_every_day
from handlers import *

from multiprocessing import Process
from flask import Flask, request

log = logging.getLogger()
app = Flask(import_name=__name__)


async def on_startup(dispatcher: Dispatcher):
    log.info('bot started...')
    await sql_start()
    await sql_drugs_db_connect()

    scheduler.add_job(check_every_day, 'interval', days=1, args=(dispatcher,))
    scheduler.start()

    dispatcher.register_message_handler(request_start_handler)
    dispatcher.register_message_handler(request_add_drug_handler)

    dispatcher.register_message_handler(request_del_drug_handler)
    dispatcher.register_message_handler(request_set_drug_id_4_del_handler, state=FSMDelDrug.id)

    dispatcher.register_message_handler(request_view_first_aid_kit)
    dispatcher.register_message_handler(request_view_first_aid_kit_expired)


def bot_start_polling():
    registry = DialogRegistry(dp)
    registry.register(add_drug_dialog)

    registry.register(view_actual_drugs_dialog)
    registry.register(del_actual_drugs_dialog)
    registry.register(view_expired_drugs_dialog)

    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


async def on_shutdown(dispatcher: Dispatcher):
    log.info('bot stopped...')
    await sql_stop()
    await sql_drugs_db_stop()


def make_drug_info_page(drug_data: dict) -> str:
    try:
        with open('DrugInfoTemplate.html', 'r', encoding='utf-8') as f:
            template_data = f.read()
            template = Template(template_data)
            return template.render(
                title=drug_data[KEY_TITLE],
                drug_group=drug_data[KEY_GROUP],
                desc=drug_data[KEY_DESC],
                contra=drug_data[KEY_CONTRA]
            )
    except Exception as e:
        print(e)


@app.get(rule='/get_drug_info')
async def get_drug_info():
    drug_info_id = request.args.get(KEY_DRUG_ID)
    await sql_drugs_db_connect()
    drug_info = await sql_get_drug_info_by_id(drug_info_id)
    return make_drug_info_page(drug_info)


@app.get(rule='/')
async def start():
    return f'<h1>Web Application for telegram bot</h1><br>Work in progress...'


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    bot_process = Process(target=bot_start_polling)
    bot_process.start()

    serving.run_simple('0.0.0.0', 8000, app)#, ssl_context='adhoc')
