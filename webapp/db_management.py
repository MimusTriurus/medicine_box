from typing import Optional, Tuple

from databases import Database

from config import DB_URL
from constants import *

database = Database(DB_URL)


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
            {KEY_DATE} TIMESTAMP NOT NULL,
            {KEY_DRUG_ID} INTEGER
        )
    ''')


async def sql_stop():
    await database.disconnect()


async def sql_add_user(user_id: int, lang_code: str):
    if not database.is_connected:
        await sql_start()

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
    if not database.is_connected:
        await sql_start()

    record = {KEY_ID: user_id}
    result = await database.fetch_all(f'SELECT * FROM {KEY_TABLE_USERS} WHERE {KEY_ID}=:{KEY_ID}', record)
    return result[0][1] if result else EN


async def sql_set_lang(user_id: int, lang_code: str):
    if not database.is_connected:
        await sql_start()

    record = {
        KEY_ID: user_id,
        KEY_LANG: lang_code
    }
    query = f'''UPDATE {KEY_TABLE_USERS} SET {KEY_LANG} = :{KEY_LANG} WHERE {KEY_ID} = :{KEY_ID}'''
    await database.execute(query, record)


async def sql_add_drug(user_id: int, data: dict, table: str = KEY_TABLE_AID_KIT) -> int:
    if not database.is_connected:
        await sql_start()

    record = {
        KEY_ID: None,
        KEY_USER_ID: user_id,
        KEY_NAME: data[KEY_NAME],
        KEY_DATE: data[KEY_DATE],
        KEY_DRUG_ID: data.get(KEY_DRUG_ID, -1)
    }
    record_id = await database.execute(
        f'''INSERT INTO {table} VALUES (
            :{KEY_ID},
            :{KEY_USER_ID},
            :{KEY_NAME},
            :{KEY_DATE},
            :{KEY_DRUG_ID}
        )''',
        record
    )
    return record_id


async def sql_get_drugs(user_id: int, table: str = KEY_TABLE_AID_KIT) -> list:
    if not database.is_connected:
        await sql_start()

    record = {KEY_USER_ID: user_id}
    result = await database.fetch_all(f'SELECT * FROM {table} WHERE {KEY_USER_ID}=:{KEY_USER_ID}', record)
    result = sorted(result, key=lambda r: r[IDX_NAME], reverse=False)
    return result


async def sql_del_drugs(drug_id: int, table: str = KEY_TABLE_AID_KIT) -> Optional[Tuple[str, str]]:
    if not database.is_connected:
        await sql_start()

    deleted_drug = await database.fetch_all(f'SELECT * FROM {table} WHERE {KEY_ID}=:{KEY_ID}', {KEY_ID: drug_id})
    if deleted_drug:
        await database.execute(f'DELETE FROM {table} WHERE {KEY_ID}=:{KEY_ID}', {KEY_ID: drug_id})
        return deleted_drug[0][IDX_NAME], deleted_drug[0][IDX_DATE]
    return None


async def sql_clear_expired_drugs(user_id: int):
    if not database.is_connected:
        await sql_start()

    await database.execute(
        f'DELETE FROM {KEY_TABLE_AID_KIT_EXPIRED} WHERE {KEY_USER_ID}=:{KEY_USER_ID}',
        {KEY_USER_ID: user_id}
    )
