from databases import Database
from config import DRUGS_DB_URL
from constants import *

KEY_ID = 'id'
KEY_URL = 'url'
KEY_TITLE = 'title'
KEY_RU_TITLE = 'ru_title'
KEY_EN_TITLE = 'en_title'
KEY_GROUP = 'drug_group'
KEY_DESC = 'desc'
KEY_CONTRA = 'contra'
KEY_SIDE_EFFECTS = 'side_effects'
KEY_SPECIAL = 'special'
TABLE_NAME = 'DRUGS_DESC'

drugs_db = Database(DRUGS_DB_URL)


async def sql_drugs_db_connect():
    await drugs_db.connect()


async def sql_drugs_db_stop():
    await drugs_db.disconnect()


async def sql_get_drug_info_by_title(drug_title: str, column: str = KEY_RU_TITLE):
    record = {column: drug_title}
    result = await drugs_db.fetch_all(f'SELECT * FROM {TABLE_NAME} WHERE {column}=:{column}', record)
    result = sorted(result, key=lambda r: r[IDX_NAME], reverse=False)
    if result:
        return result[0]
    return None


async def sql_get_drug_info_by_id(drug_id: str):
    record = {KEY_ID: drug_id}
    result = await drugs_db.fetch_all(f'SELECT * FROM {TABLE_NAME} WHERE {KEY_ID}=:{KEY_ID}', record)
    result = sorted(result, key=lambda r: r[IDX_NAME], reverse=False)
    if result:
        return result[0]
    return None