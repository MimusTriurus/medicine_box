from typing import Optional, Tuple

from databases import Database

from config import DB_URL
from constants import *
from helpers import time_is_over

database = Database(DB_URL)


async def sql_start():
    await database.connect()
    # id serial primary key,
    await database.execute(f'CREATE TABLE IF NOT EXISTS {KEY_TABLE_USERS}({KEY_ID} SERIAL PRIMARY KEY)')

    await database.execute(f'''
        CREATE TABLE IF NOT EXISTS {KEY_TABLE_AID_KIT}(
            {KEY_ID} INTEGER PRIMARY KEY AUTOINCREMENT,
            {KEY_USER_ID} INTEGER NOT NULL,
            {KEY_NAME} TEXT NOT NULL, 
            {KEY_DATE} TIMESTAMP NOT NULL
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


async def sql_add_user(user_id: int):
    record = {KEY_ID: user_id}
    user_id = await database.fetch_all(f'SELECT * FROM {KEY_TABLE_USERS} WHERE {KEY_ID}=:{KEY_ID}', values=record)
    if not user_id:
        await database.execute(f'INSERT INTO {KEY_TABLE_USERS} VALUES(:{KEY_ID})', values=record)


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
    # async with state.proxy() as data:
    record = {
        KEY_ID: None,
        KEY_USER_ID: user_id,
        KEY_NAME: data[KEY_NAME],
        KEY_DATE: data[KEY_DATE]
    }
    await database.execute(
        f'''INSERT INTO {table} VALUES (
            :{KEY_ID},
            :{KEY_USER_ID},
            :{KEY_NAME},
            :{KEY_DATE}
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
