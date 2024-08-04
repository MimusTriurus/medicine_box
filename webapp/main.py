import json
import logging

from flask import Flask, request, render_template, Response
from jinja2 import Template

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
from config import IS_IT_PROD, WEBAPP_PORT

log = logging.getLogger()
app = Flask(import_name=__name__)


def make_drug_info_page(drug_data: dict) -> str:
    try:
        with open('../webapp/templates/DrugInfoTemplate.html', 'r', encoding='utf-8') as f:
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
    return f'<h1>Web Application for telegram bot</h1><br>Work in progress...'


@app.get(rule='/get_drug_info')
async def get_drug_info():
    drug_info_id = request.args.get(KEY_DRUG_ID)
    await sql_drugs_db_connect()
    drug_info = await sql_get_drug_info_by_id(drug_info_id)
    return make_drug_info_page(drug_info)


@app.get(rule='/add_drug')
async def add_drug():
    return render_template('search.html')


@app.route('/edit', methods=['GET', 'POST'])
async def edit():
    result = []
    for drug_title in request.form:
        if len(drug_title) > 1:
            for r in await sql_get_drug_info_candidates(drug_title):
                result.append(r[0])
    return Response(json.dumps(result), mimetype='application/json')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    HOST = '0.0.0.0'
    if IS_IT_PROD:
        import waitress

        waitress.serve(app, host=HOST, port=WEBAPP_PORT)
    else:
        from werkzeug import serving

        serving.run_simple(HOST, WEBAPP_PORT, app, ssl_context='adhoc')
