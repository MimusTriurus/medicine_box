import asyncio
import logging

from aiogram.utils.executor import start_webhook

from components import bot
from config import WEBHOOK_URL, IS_LOCAL_MODE, WEBHOOK_PATH, WEBAPP_HOST, WEBAPP_PORT
from db_management import sql_start, sql_stop
from expired_drugs_checker import scheduler, check_every_day
from handlers import *


async def on_startup(dispatcher):
    await sql_start()
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await sql_stop()
    await bot.delete_webhook()


if IS_LOCAL_MODE:
    async def main():
        try:
            await sql_start()
            print('Local mode')
            scheduler.add_job(check_every_day, 'interval', hours=24, args=(bot,))
            scheduler.start()

            dp.register_message_handler(request_start_handler)
            dp.register_message_handler(request_add_drug_handler)

            dp.register_message_handler(request_set_drug_name_handler, state=FSMAddDrug.name)
            dp.register_message_handler(request_set_drug_date_handler, state=FSMAddDrug.date)

            dp.register_message_handler(request_del_drug_handler)
            dp.register_message_handler(request_set_drug_id_4_del_handler, state=FSMDelDrug.id)

            dp.register_message_handler(request_view_first_aid_kit)
            dp.register_message_handler(request_view_first_aid_kit_expired)

            await dp.start_polling()
        finally:
            await bot.close()


    asyncio.run(main())
else:
    if __name__ == '__main__':
        print('Hook mode')
        logging.basicConfig(level=logging.INFO)
        start_webhook(
            dispatcher=dp,
            webhook_path=WEBHOOK_PATH,
            skip_updates=True,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            host=WEBAPP_HOST,
            port=WEBAPP_PORT,
        )
