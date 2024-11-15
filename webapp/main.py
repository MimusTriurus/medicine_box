import datetime
import json
import logging
import re
from typing import Tuple

import requests

from flask import Flask, request, render_template, Response
from jinja2 import Template

from config import WEBAPP_PORT, VIDAL_LINK
from drugs_db_management import (
    KEY_GROUP,
    KEY_DESC,
    KEY_CONTRA,
    KEY_TITLE,
    KEY_DRUG_ID,
    KEY_EN_TITLE,
    KEY_RU_TITLE,
    sql_drugs_db_connect,
    sql_get_drug_info_by_id,
    sql_get_drug_info_candidates,
)
from constants import (
    KEY_USER_ID,
    KEY_ID,
    KEY_NAME,
    KEY_DATE,
    KEY_TABLE_AID_KIT_EXPIRED,
    KEY_TABLE_AID_KIT,
    KEY_TARGET_TABLE,
    MSG_NO_INFO,
    KEY_DRUG_DESC,
)
from db_management import sql_add_drug, sql_get_drugs, sql_del_drugs

log = logging.getLogger()
app = Flask(import_name=__name__)

pattern_price = re.compile(r'<div class="buy-table__price">.*?</div>')
pattern_order = re.compile(r'<div class="buy-table__order">.*?</div>')
pattern_img = re.compile(r'<img src="/upload.*?/>')


def make_drug_info_page(drug_data: dict) -> str:
    if not drug_data:
        return MSG_NO_INFO

    try:
        with open('templates/drug_info.html', 'r', encoding='utf-8') as f:
            template_data = f.read()
            template = Template(template_data)
            return template.render(
                title=drug_data[KEY_TITLE],
                drug_group=drug_data[KEY_GROUP],
                desc=drug_data[KEY_DESC],
                contra=drug_data[KEY_CONTRA]
            )
    except Exception as e:
        print(e)


def make_expired_drug_info_page(drug_data: dict) -> str:
    if not drug_data:
        return MSG_NO_INFO

    try:
        drug_id = drug_data[KEY_DRUG_ID]

        url = f'{VIDAL_LINK}/protec/{drug_id}'
        response = requests.get(url)
        content = ''
        if response.status_code == 200:
            content = response.text.encode('latin-1').decode('unicode_escape').replace('\\', '')

            content = re.sub(
                r'\s+',
                ' ',
                content
            )

            prices = pattern_price.findall(content)
            if not prices:
                return MSG_NO_INFO
            orders = pattern_order.findall(content)
            if not orders:
                return MSG_NO_INFO
            images = pattern_img.findall(content)
            if not images:
                return MSG_NO_INFO
            content = ''
            for i in range(len(images)):
                images[i] = images[i].replace('<img src="/upload', f'<img src="{VIDAL_LINK}/upload')
                content += f'''
                    <div class="buy-table__item">
                        <div>{images[i]}</div>
                        {prices[i]}
                        {orders[i]}
                    </div>
                    '''
        with open('templates/expired_drug_info.html', 'r', encoding='utf-8') as f:
            template_data = f.read()
            template = Template(template_data)
            return template.render(
                drug_group=drug_data[KEY_GROUP],
                content=content
            )
    except Exception as e:
        print(e)


@app.get(rule='/')
async def start():
    return render_template('index_template.html', usr_id='test_user')


async def make_drug_record(drug: dict) -> dict:
    if KEY_DRUG_ID in drug:
        info_data = await sql_get_drug_info_by_id(drug[KEY_DRUG_ID])
    else:
        info_data = None
    return {
        KEY_ID: drug[KEY_ID],
        KEY_TITLE: drug[KEY_NAME],
        KEY_DATE: drug[KEY_DATE],
        KEY_DRUG_DESC: make_drug_info_page(info_data)
    }


async def make_expired_drug_record(drug: dict) -> dict:
    info_data = await sql_get_drug_info_by_id(drug[KEY_DRUG_ID])
    return {
        KEY_ID: drug[KEY_ID],
        KEY_TITLE: drug[KEY_NAME],
        KEY_DATE: drug[KEY_DATE],
        KEY_DRUG_DESC: make_expired_drug_info_page(info_data)
    }


async def make_drug_info_record(drug: dict, desc_maker=make_drug_info_page) -> dict:
    if KEY_DRUG_ID in drug:
        info_data = await sql_get_drug_info_by_id(drug[KEY_DRUG_ID])
    else:
        info_data = None
    return {
        KEY_ID: drug[KEY_ID],
        KEY_TITLE: drug[KEY_NAME],
        KEY_DATE: drug[KEY_DATE],
        KEY_DRUG_DESC: desc_maker(info_data)
    }


@app.post(rule='/add_drug')
async def add_drug():
    drug_data = dict(request.form)
    date = datetime.datetime.strptime(drug_data[KEY_DATE], '%Y-%m').date()
    target_table = KEY_TABLE_AID_KIT
    drug_record_maker = make_drug_info_page
    if date < datetime.datetime.now().date():
        target_table = KEY_TABLE_AID_KIT_EXPIRED
        drug_record_maker = make_expired_drug_info_page

    user_id = int(drug_data[KEY_USER_ID])
    record_id = await sql_add_drug(user_id, drug_data, target_table)
    drug_data[KEY_ID] = record_id
    drug_record = await make_drug_info_record(drug_data, drug_record_maker)
    drug_record[KEY_TARGET_TABLE] = target_table
    return Response(json.dumps(drug_record), mimetype='application/json')


@app.delete(rule='/del_non_expired_drug')
async def del_non_expired_drug():
    drug_id = int(request.form[KEY_DRUG_ID])
    await sql_del_drugs(drug_id)
    return Response()


@app.delete(rule='/del_expired_drug')
async def del_expired_drug():
    drug_id = int(request.form[KEY_DRUG_ID])
    await sql_del_drugs(drug_id, KEY_TABLE_AID_KIT_EXPIRED)
    return Response()


def drug_obj_from_tuple(drug_tuple: Tuple) -> dict:
    return {
        KEY_ID: drug_tuple[0],
        KEY_USER_ID: drug_tuple[1],
        KEY_NAME: drug_tuple[2],
        KEY_DATE: drug_tuple[3],
        KEY_DRUG_ID: drug_tuple[4]
    }


@app.get(rule='/non_expired_drugs')
async def non_expired_drugs():
    usr_id = int(request.args['usr_id'])
    drugs = []
    for drug in await sql_get_drugs(usr_id):
        drug_record = await make_drug_info_record(drug_obj_from_tuple(drug), make_drug_info_page)
        drugs.append(drug_record)
    return Response(json.dumps(drugs), mimetype='application/json')


@app.get(rule='/expired_drugs')
async def expired_drugs():
    usr_id = int(request.args['usr_id'])
    drugs = []
    for drug in await sql_get_drugs(usr_id, table=KEY_TABLE_AID_KIT_EXPIRED):
        drug_record = await make_drug_info_record(drug_obj_from_tuple(drug), make_expired_drug_info_page)
        drugs.append(drug_record)
    return Response(json.dumps(drugs), mimetype='application/json')


def rus_match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')) -> bool:
    return not alphabet.isdisjoint(text.lower())


@app.route('/edit', methods=['GET', 'POST'])
async def edit():
    result = dict()
    for drug_part_title in request.form:
        if len(drug_part_title) > 1:
            target_column = KEY_RU_TITLE if rus_match(drug_part_title) else KEY_EN_TITLE
            for r in await sql_get_drug_info_candidates(drug_part_title, target_column):
                drug_title = r[0]
                drug_id = r[1]
                result[drug_title] = drug_id
    return Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    HOST = '0.0.0.0'
    app.run(host=HOST, port=WEBAPP_PORT)
