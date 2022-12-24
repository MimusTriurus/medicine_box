from aiogram import Bot, types

from db_management import sql_check_expired_drugs

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from helpers import make_expired_drug_message

scheduler = AsyncIOScheduler()


async def check_every_day(bot: Bot):
    print('Checking...')
    expired_drugs = await sql_check_expired_drugs()

    for drug in expired_drugs:
        usr_id = drug[1]
        await bot.send_message(usr_id, make_expired_drug_message(drug), parse_mode=types.ParseMode.HTML)
