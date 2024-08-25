import json
import logging

from cryptography.fernet import Fernet
from flask import Flask, request, render_template, Response
from jinja2 import Template

from config import IS_IT_PROD, WEBAPP_PORT, PASSWORD
from drugs_db_management import (
    KEY_GROUP,
    KEY_DESC,
    KEY_CONTRA,
    KEY_TITLE,
    KEY_DRUG_ID,
    sql_drugs_db_connect,
    sql_get_drug_info_by_id,
    sql_get_drug_info_candidates
)

log = logging.getLogger()
app = Flask(import_name=__name__)


def make_drug_info_page(drug_data: dict) -> str:
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
    return render_template('index.html')


@app.get(rule='/get_drug_info')
async def get_drug_info():
    drug_info_id = request.args.get(KEY_DRUG_ID)
    await sql_drugs_db_connect()
    drug_info = await sql_get_drug_info_by_id(drug_info_id)
    return make_drug_info_page(drug_info)


@app.get(rule='/add_drug')
async def add_drug():
    return render_template('add_drug.html')


@app.get(rule='/non_expired_drugs')
async def non_expired_drugs():
    key = request.args['key'].encode()
    cipher_suite = Fernet(PASSWORD.encode())
    decoded_key = cipher_suite.decrypt(key)

    drugs = []
    for i in range(1, 31):
        drugs.append(
            {
                'id': i,
                'title': f'drug_{i}',
                'date': f'{i}.01.2024'
            }
        )
    return render_template('non_expired_drugs.html', title='None-expired drugs', drugs=drugs)


def sanitize_drug_title(input_value: str) -> str:
    output = input_value.replace('инструкция по применению', '')
    output = output.replace('ОПИСАНИЕ', '')
    output = output.rstrip()
    return output


@app.route('/edit', methods=['GET', 'POST'])
async def edit():
    result = dict()
    for drug_part_title in request.form:
        if len(drug_part_title) > 1:
            for r in await sql_get_drug_info_candidates(drug_part_title):
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
