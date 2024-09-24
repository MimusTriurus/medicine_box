import datetime
import json
import logging

from flask import Flask, request, render_template, Response
from jinja2 import Template

from config import IS_IT_PROD, WEBAPP_PORT
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
)
from db_management import sql_add_drug, sql_get_drugs, sql_del_drugs

log = logging.getLogger()
app = Flask(import_name=__name__)


# obsolete
def make_drug_info_page(drug_data: dict) -> str:
    if not drug_data:
        return "No info. Sorry."

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


@app.get(rule='/')
async def start():
    return render_template('index_template.html', usr_id="test_user")


# obsolete
@app.get(rule='/get_drug_info')
async def get_drug_info():
    drug_info_id = request.args.get(KEY_DRUG_ID)
    await sql_drugs_db_connect()
    drug_info = await sql_get_drug_info_by_id(drug_info_id)
    return make_drug_info_page(drug_info)


async def make_drug_record(drug: dict) -> dict:
    info_data = await sql_get_drug_info_by_id(drug[KEY_DRUG_ID])
    return {
        KEY_ID: drug[KEY_ID],
        KEY_TITLE: drug[KEY_NAME],
        KEY_DATE: drug[KEY_DATE],
        'description': make_drug_info_page(info_data)
    }


@app.post(rule='/add_drug')
async def add_drug():
    drug_data = dict(request.form)
    date = datetime.datetime.strptime(drug_data[KEY_DATE], '%Y-%m').date()
    target_table = KEY_TABLE_AID_KIT
    if date < datetime.datetime.now().date():
        target_table = KEY_TABLE_AID_KIT_EXPIRED
    user_id = int(drug_data[KEY_USER_ID])
    record_id = await sql_add_drug(user_id, drug_data, target_table)
    drug_data[KEY_ID] = record_id
    drug_record = await make_drug_record(drug_data)
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


@app.get(rule='/non_expired_drugs')
async def non_expired_drugs():
    usr_id = int(request.args['usr_id'])
    drugs = []
    for drug in await sql_get_drugs(usr_id):
        drug_record = await make_drug_record(drug)
        drugs.append(drug_record)
    return Response(json.dumps(drugs), mimetype='application/json')


@app.get(rule='/expired_drugs')
async def expired_drugs():
    usr_id = int(request.args['usr_id'])
    drugs = []
    for drug in await sql_get_drugs(usr_id, table=KEY_TABLE_AID_KIT_EXPIRED):
        drug_record = await make_drug_record(drug)
        drugs.append(drug_record)
    return Response(json.dumps(drugs), mimetype='application/json')


def sanitize_drug_title(input_value: str) -> str:
    output = input_value.replace('инструкция по применению', '')
    output = output.replace('ОПИСАНИЕ', '')
    output = output.rstrip()
    return output


def rus_match(text, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')) -> bool:
    return not alphabet.isdisjoint(text.lower())


@app.route('/edit', methods=['GET', 'POST'])
async def edit():
    result = dict()
    for drug_part_title in request.form:
        if len(drug_part_title) > 1:
            target_column = KEY_RU_TITLE if rus_match(drug_part_title) else KEY_EN_TITLE
            for r in await sql_get_drug_info_candidates(drug_part_title, target_column):
                drug_title = sanitize_drug_title(r[0])
                drug_id = r[1]
                result[drug_title] = drug_id
    return Response(json.dumps(result), mimetype='application/json')


@app.route('/test', methods=['GET', 'POST'])
async def test():
    r = request
    print(request.data)
    return Response()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    HOST = '0.0.0.0'
    if IS_IT_PROD:
        import waitress
        waitress.serve(app, host=HOST, port=WEBAPP_PORT)
    else:
        from werkzeug import serving
        serving.run_simple(HOST, WEBAPP_PORT, app, ssl_context='adhoc')
