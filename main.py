import logging

from aiogram import Dispatcher
from aiogram.utils.executor import start_webhook

from components import bot
from config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, TOKEN
from db_management import sql_start, sql_stop
from expired_drugs_checker import scheduler, check_every_day
from handlers import *

log = logging.getLogger()


async def on_startup(dispatcher: Dispatcher):
    log.info('on startup')
    # await sql_start()
    # log.info('sql started')
    # scheduler.add_job(check_every_day, 'interval', hours=24, args=(bot,))
    # scheduler.start()
    try:
        log.info(f'try to set webhook: {WEBHOOK_URL}')
        await dispatcher.bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)
        log.info(f'end set of webhook: {WEBHOOK_URL}')
    except Exception as e:
        log.error(e)


async def on_shutdown(dispatcher: Dispatcher):
    log.info('on shutdown')
    await sql_stop()
    await dispatcher.bot.delete_webhook()

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    log.info(f'***********')
    log.info(f'{TOKEN}')
    log.info(f'{WEBAPP_PORT}')
    log.info(f'{WEBHOOK_PATH}')
    log.info(f'***********')
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
