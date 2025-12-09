import datetime
import json
import logging
from typing import Tuple, Optional

from flask import Flask, request, render_template, Response, url_for
from apscheduler.schedulers.background import BackgroundScheduler
from asyncio import run
from jinja2 import Template, Environment, FileSystemLoader

from config import WEBAPP_PORT, VIDAL_LINK
from constants import *
from db_management import sql_add_drug, sql_get_drugs, sql_del_drugs, sql_check_expired_drugs, \
    sql_get_drug_by_datamatrix_code
from drugs_db_management import (
    KEY_GROUP,
    KEY_DESC,
    KEY_CONTRA,
    KEY_TITLE,
    KEY_DRUG_ID,
    KEY_EN_TITLE,
    KEY_RU_TITLE,
    sql_get_drug_info_by_id,
    sql_get_drug_info_candidates,
)
from localization.localization_keys import *
from queue_publisher import QueuePublisher
from crpt import Crpt

log = logging.getLogger()
app = Flask(import_name=__name__)
scheduler = BackgroundScheduler()


def drug_obj_from_tuple(drug_tuple: Tuple) -> dict:
    return {
        KEY_ID: drug_tuple[0],
        KEY_USER_ID: drug_tuple[1],
        KEY_NAME: drug_tuple[2],
        KEY_DATE: drug_tuple[3],
        KEY_DRUG_ID: drug_tuple[4]
    }


async def check_expired_drugs():
    expired_drugs_tuples = await sql_check_expired_drugs()
    if expired_drugs_tuples:
        expired_drugs_lst = list()
        for drug_tuple in expired_drugs_tuples:
            drug_obj = drug_obj_from_tuple(drug_tuple)
            expired_drugs_lst.append(drug_obj)

        make_expired_drug_record_4_bot(
            {
                KEY_EXPIRED: expired_drugs_lst
            }
        )

job = scheduler.add_job(
    lambda: run(check_expired_drugs()),
    "cron",
    hour=23,
    minute=00
)

def get_localization_data(lang: str) -> Optional[dict]:
    loc = localizers.get(lang, None)
    if not loc:
        return None
    localization_data = {
        KEY_JAN: loc.gettext(ID_TXT_JANUARY),
        KEY_FEB: loc.gettext(ID_TXT_FEBRUARY),
        KEY_MAR: loc.gettext(ID_TXT_MARCH),
        KEY_APR: loc.gettext(ID_TXT_APRIL),
        KEY_MAY: loc.gettext(ID_TXT_MAY),
        KEY_JUN: loc.gettext(ID_TXT_JUNE),
        KEY_JUL: loc.gettext(ID_TXT_JULY),
        KEY_AUG: loc.gettext(ID_TXT_AUGUST),
        KEY_SEP: loc.gettext(ID_TXT_SEPTEMBER),
        KEY_OCT: loc.gettext(ID_TXT_OCTOBER),
        KEY_NOV: loc.gettext(ID_TXT_NOVEMBER),
        KEY_DEC: loc.gettext(ID_TXT_DECEMBER),
        KEY_NAME_OF_DRUG: loc.gettext(ID_TXT_DRUG_NAME),
        KEY_NON_EXPIRED: loc.gettext(ID_TXT_NON_EXPIRED),
        KEY_EXPIRED: loc.gettext(ID_TXT_EXPIRED),
        KEY_DRUG_NOT_AVAILABLE_4_BUY: loc.gettext(ID_TXT_DRUG_CANT_BUY)
    }

    return localization_data


def get_localization():
    result = dict()

    result[EN] = get_localization_data(EN)
    result[RU] = get_localization_data(RU)
    json_str = json.dumps(result)
    return json_str


localization_data = get_localization()


def rus_match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')) -> bool:
    return not alphabet.isdisjoint(text.lower())


def make_not_expired_drug_info_page(drug_data: dict) -> str:
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


def get_drugstores(drug_id: str) -> Tuple[list, list, list, list]:
    import requests
    url = f'{VIDAL_LINK}/protec/{drug_id}'
    response = requests.get(url)
    if response.status_code == 200:
        content = response.text.encode('latin-1').decode('unicode_escape').replace('\\', '')

        content = re.sub(
            r'\s+',
            ' ',
            content
        )

        prices = pattern_price_html.findall(content)
        orders = pattern_order_html.findall(content)
        images = pattern_img_html.findall(content)
        stores = pattern_store.findall(content)
        return prices, orders, images, stores
    return [], [], [], []


def make_expired_drug_info_page(drug_data: dict, template_file='templates/expired_drug_info.html') -> str:
    if not drug_data:
        return MSG_NO_INFO

    try:
        content = ''
        if KEY_PRICES in drug_data:
            prices = drug_data[KEY_PRICES]
            orders = drug_data[KEY_ORDERS]
            images = drug_data[KEY_IMAGES]

            if prices and orders and images:
                for i in range(len(images)):
                    images[i] = images[i].replace('<img src="/upload', f'<img src="{VIDAL_LINK}/upload')
                    content += f'''
                        <div class="buy-table__item">
                            <div>{images[i]}</div>
                            {prices[i]}
                            {orders[i]}
                        </div>
                        '''

        if not content:
            content = f'''
            <br>
            <label data-i18n-key="drug_not_available_for_purchase"></label>
            '''
        with open(template_file, 'r', encoding='utf-8') as f:
            template_data = f.read()
            template = Environment(loader=FileSystemLoader('templates/')).from_string(template_data)
            template.globals['url_for'] = url_for
            html_str = template.render(
                drug_group=drug_data[KEY_GROUP],
                content=content,
                localization=localization_data
            )
            return html_str
    except Exception as e:
        print(f'Error: {e}')
        return MSG_NO_INFO


async def make_drug_info_record(drug: dict, desc_maker=make_not_expired_drug_info_page) -> dict:
    drug_info = None
    if KEY_DRUG_ID in drug:
        drug_info = await sql_get_drug_info_by_id(drug[KEY_DRUG_ID])
        if drug_info:
            drug_info = dict(drug_info)
            drug_info.update(drug)
    return {
        KEY_ID: drug[KEY_ID],
        KEY_TITLE: drug[KEY_NAME],
        KEY_DATE: drug[KEY_DATE],
        KEY_DRUG_DESC: desc_maker(drug_info) if desc_maker else ''
    }


def make_expired_drug_record_4_bot(drug_data: dict):
    try:
        qp = QueuePublisher()
        qp.qp_put_2_queue(drug_data)
        # del qp
    except Exception as e:
        print(f'Error on putting drug data to the queue: {e}')


@app.get(rule='/')
async def start():
    return render_template(
        'index_template.html',
        localization=localization_data
    )


@app.get(rule='/first_aid_kit_info')
async def first_aid_kit_info():
    return render_template('first_aid_med_kit_example.html')


@app.post(rule='/add_drug')
async def add_drug():
    drug_data = dict(request.form)
    date = datetime.datetime.strptime(drug_data[KEY_DATE], DATE_FORMAT).date()
    target_table = KEY_TABLE_AID_KIT
    drug_record_maker = make_not_expired_drug_info_page

    if date < datetime.datetime.now().date(): 
        drug_data[KEY_PRICES] = []
        drug_data[KEY_ORDERS] = []
        drug_data[KEY_IMAGES] = []
        drug_data[KEY_STORES] = []

        if KEY_DRUG_ID in drug_data:
            drug_id = drug_data[KEY_DRUG_ID]
            prices, orders, images, stores = get_drugstores(drug_id)
            drug_data[KEY_PRICES] = prices
            drug_data[KEY_ORDERS] = orders
            drug_data[KEY_IMAGES] = images
            drug_data[KEY_STORES] = stores
        
        expired_drug = {
            KEY_EXPIRED: [
                drug_data
            ]
        }

        make_expired_drug_record_4_bot(expired_drug)

        target_table = KEY_TABLE_AID_KIT_EXPIRED
        drug_record_maker = make_expired_drug_info_page

    user_id = int(drug_data[KEY_USER_ID])
    record_id = await sql_add_drug(user_id, drug_data, target_table)
    drug_data[KEY_ID] = record_id
    drug_record = await make_drug_info_record(drug_data, drug_record_maker)
    drug_record[KEY_TARGET_TABLE] = target_table
    return Response(json.dumps(drug_record), mimetype='application/json')


@app.post(rule='/add_scanned_drug')
async def add_scanned_drug():
    drug_data = dict(request.form)
    tg_user = drug_data.get('tg_user', '')
    raw_dm = drug_data.get('dm', '')
    if tg_user and raw_dm:
        drug_by_dmcode = await sql_get_drug_by_datamatrix_code(tg_user, raw_dm)
        if not drug_by_dmcode:
            drug_by_dmcode = await sql_get_drug_by_datamatrix_code(tg_user, raw_dm, KEY_TABLE_AID_KIT_EXPIRED)

        dm_code = raw_dm.split(' ')
        if dm_code:
            crpt = Crpt()
            drug_data = crpt.info_from_datamatrix(dm_code[0])
            product_name = drug_data.get('productName', None)
            exp_date = drug_data.get('expDate', None)
            drug_info = drug_data.get('drugsData', None)
            drug_desc: str = ''
            if drug_info:
                vidal_data = drug_info.get('vidalData', None)
                if vidal_data:
                    drug_desc = vidal_data.get('phKinetics', '')
                    drug_desc = re.sub(r'<.*?>', '', drug_desc)

            if product_name and exp_date:
                drug_candidates = await sql_get_drug_info_candidates(product_name)
                if drug_candidates:
                    found_drug = drug_candidates[0]
                    drug_title = found_drug[0]
                    drug_id = found_drug[1]
                    date_candidates = re.findall('(\d{4}-\d{2}-\d{2}).+', exp_date)
                    if date_candidates:
                        date_object = datetime.datetime.strptime(date_candidates[0], '%Y-%m-%d')
                        result = {
                            KEY_DRUG_ID: drug_id,
                            KEY_NAME: drug_title,
                            KEY_DATE: date_object.strftime(DATE_FORMAT),
                            KEY_DRUG_DESC: drug_desc,
                            KEY_DATAMATRIX: raw_dm,
                            KEY_EXPIRED: TRUE if datetime.datetime.now() >= date_object else FALSE,
                            KEY_EXIST: TRUE if drug_by_dmcode else FALSE
                        }
                        return Response(json.dumps(result), mimetype='application/json')
    return Response(json.dumps({}), mimetype='application/json')


@app.delete(rule='/del_non_expired_drug')
async def del_non_expired_drug():
    drug_id = request.form[KEY_DRUG_ID]
    await sql_del_drugs(drug_id)
    return Response()


@app.get(rule='/get_drug_stores')
async def get_drug_stores():
    drug_id = request.args.get(KEY_DRUG_ID)
    drug_info = await sql_get_drug_info_by_id(drug_id)
    title = ''
    if drug_info:
        title = drug_info[KEY_TITLE]
    prices, orders, images, stores = get_drugstores(drug_id)
    drug_data = {KEY_GROUP: title, KEY_PRICES: prices, KEY_ORDERS: orders, KEY_IMAGES: images, KEY_STORES: stores}
    return make_expired_drug_info_page(drug_data, 'templates/drug_stores_info.html')


@app.delete(rule='/del_expired_drug')
async def del_expired_drug():
    drug_id = request.form[KEY_DRUG_ID]
    await sql_del_drugs(drug_id, KEY_TABLE_AID_KIT_EXPIRED)
    return Response()


@app.get(rule='/non_expired_drugs')
async def non_expired_drugs():
    usr_id = request.args.get(KEY_USER_ID)
    drugs = []
    if usr_id:
        for drug in await sql_get_drugs(usr_id):
            drug_obj = drug_obj_from_tuple(drug)
            drug_record = await make_drug_info_record(drug_obj, make_not_expired_drug_info_page)
            drugs.append(drug_record)
    return Response(json.dumps(drugs), mimetype='application/json')


@app.get(rule='/expired_drugs')
async def expired_drugs():
    usr_id = request.args.get(KEY_USER_ID)
    drugs = []
    if usr_id:
        for drug in await sql_get_drugs(usr_id, table=KEY_TABLE_AID_KIT_EXPIRED):
            drug_id = drug[KEY_DRUG_ID]
            # оптимизировать!!!
            prices, orders, images, stores = get_drugstores(drug_id)
            drug_data = drug_obj_from_tuple(drug)
            drug_data[KEY_PRICES] = prices
            drug_data[KEY_ORDERS] = orders
            drug_data[KEY_IMAGES] = images
            drug_data[KEY_STORES] = stores

            drug_record = await make_drug_info_record(drug_data, make_expired_drug_info_page)
            drugs.append(drug_record)
    return Response(json.dumps(drugs), mimetype='application/json')


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
    scheduler.start()
    HOST = '0.0.0.0'
    app.run(host=HOST, port=WEBAPP_PORT)
