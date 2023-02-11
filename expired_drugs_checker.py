from aiogram import Bot, types, Dispatcher

from db_management import sql_check_expired_drugs, sql_get_lang

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from localization.string_builder import make_expired_drug_message

scheduler = AsyncIOScheduler()


async def check_every_day(dispatcher: Dispatcher):
    expired_drugs = await sql_check_expired_drugs()
    for drug in expired_drugs:
        usr_id = drug[1]
        drug_name = drug[2]
        expired_date = drug[3]
        lang = await sql_get_lang(usr_id)
        await dispatcher.bot.send_message(
            usr_id,
            make_expired_drug_message(lang, drug_name, expired_date),
            parse_mode=types.ParseMode.HTML
        )
