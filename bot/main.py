import logging
from multiprocessing import Process

from aiogram import Dispatcher
from aiogram.utils.executor import start_polling
from aiogram_dialog import DialogRegistry

from db_management import sql_start, sql_stop
from dialogs.add_drug_dialog import add_drug_dialog
from dialogs.view_drugs_dialog import view_actual_drugs_dialog, del_actual_drugs_dialog, view_expired_drugs_dialog
from expired_drugs_checker import scheduler, check_every_day
from handlers import *

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


async def on_startup(dispatcher: Dispatcher):
    log.info('bot started...')
    await sql_start()

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


def main():
    bot_process = Process(target=bot_start_polling)
    bot_process.start()
    return 0


if __name__ == '__main__':
    exit(main())
