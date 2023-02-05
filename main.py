import logging

from aiogram import Dispatcher
from aiogram.utils.executor import start_polling
from aiogram_dialog import DialogRegistry

from db_management import sql_start, sql_stop
from dialogs.add_drug_dialog import add_drug_dialog
from dialogs.view_drugs_dialog import view_actual_drugs_dialog, del_actual_drugs_dialog, view_expired_drugs_dialog
from expired_drugs_checker import scheduler, check_every_day
from handlers import *


log = logging.getLogger()


async def on_startup(dispatcher: Dispatcher):
    log.info('bot started...')
    await sql_start()

    scheduler.add_job(check_every_day, 'interval', minutes=1, args=(dispatcher,))
    scheduler.start()

    dispatcher.register_message_handler(request_start_handler)
    dispatcher.register_message_handler(request_add_drug_handler)

    dispatcher.register_message_handler(request_del_drug_handler)
    dispatcher.register_message_handler(request_set_drug_id_4_del_handler, state=FSMDelDrug.id)

    dispatcher.register_message_handler(request_view_first_aid_kit)
    dispatcher.register_message_handler(request_view_first_aid_kit_expired)


async def on_shutdown(dispatcher: Dispatcher):
    log.info('bot stopped...')
    await sql_stop()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)

    registry = DialogRegistry(dp)
    registry.register(add_drug_dialog)

    registry.register(view_actual_drugs_dialog)
    registry.register(del_actual_drugs_dialog)
    registry.register(view_expired_drugs_dialog)

    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
