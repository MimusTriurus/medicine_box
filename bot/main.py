import logging

from aiogram import Dispatcher
from aiogram.utils.executor import start_polling
from aiogram_dialog import DialogRegistry

from db_management import sql_start, sql_stop
from expired_drugs_checker import scheduler, check_every_day
from handlers import *

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


async def on_startup(dispatcher: Dispatcher):
    log.info('bot started...')
    await sql_start()

    # scheduler.add_job(check_every_day, 'interval', minutes=1, args=(dispatcher,))
    scheduler.add_job(check_every_day, 'interval', days=30, args=(dispatcher,))
    scheduler.start()

    dispatcher.register_message_handler(request_start_handler)


def bot_start_polling():
    registry = DialogRegistry(dp)
    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


async def on_shutdown(dispatcher: Dispatcher):
    log.info('bot stopped...')
    await sql_stop()


def main():
    bot_start_polling()
    return 0


if __name__ == '__main__':
    exit(main())
