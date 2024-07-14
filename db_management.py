from typing import Optional, Tuple

from databases import Database

from config import DB_URL, DRUGS_DB_URL
from constants import *
from helpers import time_is_over

database = Database(DB_URL)
drugs_db = Database(DRUGS_DB_URL)


async def sql_start():
    await database.connect()
    # id serial primary key,
    await database.execute(f'''
        CREATE TABLE IF NOT EXISTS {KEY_TABLE_USERS}(
            {KEY_ID} INTEGER SERIAL PRIMARY KEY,
            {KEY_LANG} TEXT NOT NULL
        )
    ''')

    await database.execute(f'''
        CREATE TABLE IF NOT EXISTS {KEY_TABLE_AID_KIT}(
            {KEY_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {KEY_USER_ID} INTEGER NOT NULL,
            {KEY_NAME} TEXT NOT NULL,
            {KEY_DATE} TIMESTAMP NOT NULL,
            {KEY_DRUG_ID} INTEGER
        )
    ''')

    await database.execute(f'''
        CREATE TABLE IF NOT EXISTS {KEY_TABLE_AID_KIT_EXPIRED}(
            {KEY_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {KEY_USER_ID} INTEGER NOT NULL,
            {KEY_NAME} TEXT NOT NULL, 
            {KEY_DATE} TIMESTAMP NOT NULL
        )
    ''')


async def sql_stop():
    await database.disconnect()


async def sql_add_user(user_id: int, lang_code: str):
    record = {
        KEY_ID: user_id,
    }
    user_id_found = await database.fetch_all(f'SELECT * FROM {KEY_TABLE_USERS} WHERE {KEY_ID}=:{KEY_ID}', values=record)
    if not user_id_found:
        record = {
            KEY_ID: user_id,
            KEY_LANG: lang_code
        }
        await database.execute(
            f'''INSERT INTO {KEY_TABLE_USERS} VALUES(
                :{KEY_ID}, 
                :{KEY_LANG}
            )''',
            record
        )
    else:
        await sql_set_lang(user_id, lang_code)


async def sql_get_lang(user_id: int) -> str:
    record = {KEY_ID: user_id}
    result = await database.fetch_all(f'SELECT * FROM {KEY_TABLE_USERS} WHERE {KEY_ID}=:{KEY_ID}', record)
    return result[0][1] if result else EN


async def sql_set_lang(user_id: int, lang_code: str):
    record = {
        KEY_ID: user_id,
        KEY_LANG: lang_code
    }
    query = f'''UPDATE {KEY_TABLE_USERS} SET {KEY_LANG} = :{KEY_LANG} WHERE {KEY_ID} = :{KEY_ID}'''
    await database.execute(query, record)


async def sql_check_expired_drugs():
    result = list()
    expired_candidates = await database.fetch_all(f'SELECT * FROM {KEY_TABLE_USERS}')
    for ret in expired_candidates:
        usr_id = ret[IDX_ID]
        users_drugs = await database.fetch_all(
            f'''SELECT * FROM {KEY_TABLE_AID_KIT} WHERE {KEY_USER_ID}=:{KEY_USER_ID}''',
            {KEY_USER_ID: usr_id}
        )
        for drug in users_drugs:
            drug_expiration_date = drug[IDX_DATE]
            if time_is_over(drug_expiration_date):
                await database.execute(f'DELETE FROM {KEY_TABLE_AID_KIT} WHERE {KEY_ID}=:{KEY_ID}', {KEY_ID: drug[IDX_ID]})
                record = {KEY_ID: None, KEY_USER_ID: drug[IDX_USR_ID], KEY_NAME: drug[IDX_NAME], KEY_DATE: drug[IDX_DATE]}
                await database.execute(
                    f'''INSERT INTO {KEY_TABLE_AID_KIT_EXPIRED} VALUES (
                        :{KEY_ID},
                        :{KEY_USER_ID},
                        :{KEY_NAME},
                        :{KEY_DATE}
                    )''',
                    record
                )
                result.append(drug)
    return result


async def sql_add_drug(user_id: int, data: dict, table: str = KEY_TABLE_AID_KIT):
    record = {
        KEY_ID: None,
        KEY_USER_ID: user_id,
        KEY_NAME: data[KEY_NAME],
        KEY_DATE: data[KEY_DATE],
        KEY_DRUG_ID: data[KEY_DRUG_ID]
    }
    await database.execute(
        f'''INSERT INTO {table} VALUES (
            :{KEY_ID},
            :{KEY_USER_ID},
            :{KEY_NAME},
            :{KEY_DATE},
            :{KEY_DRUG_ID}
        )''',
        record
    )


async def sql_get_drugs(user_id: int, table: str = KEY_TABLE_AID_KIT) -> list:
    record = {KEY_USER_ID: user_id}
    result = await database.fetch_all(f'SELECT * FROM {table} WHERE {KEY_USER_ID}=:{KEY_USER_ID}', record)
    result = sorted(result, key=lambda r: r[IDX_NAME], reverse=False)
    return result


async def sql_del_drugs(drug_id: int, table: str = KEY_TABLE_AID_KIT) -> Optional[Tuple[str, str]]:
    deleted_drug = await database.fetch_all(f'SELECT * FROM {table} WHERE {KEY_ID}=:{KEY_ID}', {KEY_ID: drug_id})
    if deleted_drug:
        await database.execute(f'DELETE FROM {table} WHERE {KEY_ID}=:{KEY_ID}', {KEY_ID: drug_id})
        return deleted_drug[0][IDX_NAME], deleted_drug[0][IDX_DATE]
    return None


async def sql_clear_expired_drugs(user_id: int):
    await database.execute(
        f'DELETE FROM {KEY_TABLE_AID_KIT_EXPIRED} WHERE {KEY_USER_ID}=:{KEY_USER_ID}',
        {KEY_USER_ID: user_id}
    )
