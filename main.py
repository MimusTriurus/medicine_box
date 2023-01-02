import logging

from aiogram.utils.executor import start_webhook

from components import bot
from config import WEBHOOK_URL, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT, TOKEN
from db_management import sql_start, sql_stop
from expired_drugs_checker import scheduler, check_every_day
from handlers import *

log = logging.getLogger()


async def on_startup(dispatcher):
    log.info('on startup')
    await sql_start()
    # scheduler.add_job(check_every_day, 'interval', hours=24, args=(bot,))
    # scheduler.start()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    log.info('on shutdown')
    await sql_stop()
    await bot.delete_webhook()

if __name__ == '__main__':
    log.info(f'{TOKEN}')
    logging.basicConfig(level=logging.INFO)
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        loop=True,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
