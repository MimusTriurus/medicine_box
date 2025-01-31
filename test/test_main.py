import re
import json
from datetime import datetime

import requests


def re_test():
    # <div class="buy-table__price">(.+)руб\. </div>
    text = ' <!--noindex--> <div> <div id="protec-table" class="buy-header pharmacy-company-uteka"> <span class="buy-header__pharmacy-name">Заказать в Ютеке</span> <img src="/upload/photo/logo-new.png?v21" alt="Ютеке" style="width:85px;height:25px;"/> </div> <div class="buy-table pharmacy"> <div class="buy-table__item"> <div class="buy-table__title"> Евра, 203 мкг+33.9 мкг/24 ч, пластырь трансдермальный, 3 шт. </div> <div class="buy-table__price"> от 1,120 руб. </div> <div class="buy-table__order"> <a rel="nofollow" href="https://uteka.ru/product/evra-288929/?utm_source=vidal&amp;utm_medium=cpc&amp;utm_campaign=https://www.vidal.ru/drugs/evra__6659" target="_blank" class="to-ga" data-code="uteka" data-id="212710"> <button class="base-button">Заказать</button> </a> </div> <div class="buy-table__vendor"> Johnson &amp; Johnson </div> </div> </div> <div style="color: gray; padding: 10px;"> Москва </div> </div> <div> <div id="protec-table" class="buy-header pharmacy-company-planet-health"> <span class="buy-header__pharmacy-name">Заказать в аптеке Планета Здоровья</span> <img src="/upload/photo/planeta.png?v21" alt="аптеке Планета Здоровья" style="width:106px;height:25px;"/> </div> <div class="buy-table pharmacy"> <div class="buy-table__item"> <div class="buy-table__title"> Евра пластырь трансдермальный 203 мкг+33.9 мкг.24 ч 3 шт </div> <div class="buy-table__price"> от 1,252 руб. </div> <div class="buy-table__order"> <a rel="nofollow" href="https://planetazdorovo.ru/ges/25356203/?utm_source=vidal.ru&amp;utm_medium=cpc&amp;utm_campaign=https://www.vidal.ru/drugs/evra__6659" target="_blank" class="to-ga" data-code="planet-health" data-id="215822"> <button class="base-button">Заказать</button> </a> </div> <div class="buy-table__vendor"> ЛТС Ломанн Терапи-Зистеме АГ, Германия </div> </div> </div> <div style="color: gray; padding: 10px;"> Москва </div> </div> <i style="display: none" id="regionFound" data-value="Нет"></i> <i style="display: none" id="regionTitle" data-value="Москва"></i> <i style="display: none" id="cityTitle" data-value="Москва"></i> <i style="display: none" id="districtTitle" data-value="Центральный федеральный округ"></i> <i style="display: none" id="regionIp" data-value="176.25.80.24"></i> <!--noindex--> '

    pattern_price = re.compile(r'<div class="buy-table__price">.*?</div>')
    pattern_order = re.compile(r'<div class="buy-table__order">.*?</div>')
    pattern_img = re.compile(r'<img src="/upload.*?/>')
    # <img src="/upload'
    match = pattern_price.findall(text)
    print(match)
    match = pattern_order.findall(text)
    print(match)
    match = pattern_img.findall(text)
    print(match)


def mq_test():
    import pika

    connection_params = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials(
            username='guest',
            password='guest'
        )
    )

    connection = pika.BlockingConnection(connection_params)

    channel = connection.channel()

    queue_name = 'test'

    channel.queue_declare(queue=queue_name, durable=True)

    message = {
        'usr_id': 486190703,
        'drug_name': 'Евра (Evra)',
        'date': '2024-9',
        'drug_id': 25611
    }

    channel.basic_publish(
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message)
    )

    print(f"Sent: '{message}'")

    connection.close()

    return 0


def mq_test_receiver():
    import pika

    connection_params = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials(
            username='guest',
            password='guest'
        )
    )

    connection = pika.BlockingConnection(connection_params)
    channel = connection.channel()
    queue_name = 'test'

    r = channel.basic_get(queue_name, True)
    print(f'=> {r[2]}')


def extract_price_and_link():
    price_text = '<div class="buy-table__price"> от 553 руб. </div>'
    link_text = '<div class="buy-table__order"> <a rel="nofollow" href="https://planetazdorovo.ru/ges/1483799/?utm_source=vidal.ru&amp;utm_medium=cpc&amp;utm_campaign=https://www.vidal.ru/drugs/advantan__8" target="_blank" class="to-ga" data-code="planet-health" data-id="214546"> <button class="base-button">Заказать</button> </a> </div>'
    text = ' <!--noindex--> <div> <div id="protec-table" class="buy-header pharmacy-company-planet-health"> <span class="buy-header__pharmacy-name">Заказать в аптеке Планета Здоровья</span> <img src="/upload/photo/planeta.png?v21" alt="аптеке Планета Здоровья" style="width:106px;height:25px;"/> </div> <div class="buy-table pharmacy"> <div class="buy-table__item"> <div class="buy-table__title"> Адвантан крем наружн. 0.1% 15г туба </div> <div class="buy-table__price"> от 553 руб. </div> <div class="buy-table__order"> <a rel="nofollow" href="https://planetazdorovo.ru/ges/1483799/?utm_source=vidal.ru&amp;utm_medium=cpc&amp;utm_campaign=https://www.vidal.ru/drugs/advantan__8" target="_blank" class="to-ga" data-code="planet-health" data-id="214546"> <button class="base-button">Заказать</button> </a> </div> <div class="buy-table__vendor"> ЛЕО Фарма Мануфэкчуринг Итали С.р.л., Италия </div> </div> </div> <div style="color: gray; padding: 10px;"> Москва </div> </div> <div> <div id="protec-table" class="buy-header pharmacy-company-uteka"> <span class="buy-header__pharmacy-name">Заказать в Ютеке</span> <img src="/upload/photo/logo-new.png?v21" alt="Ютеке" style="width:85px;height:25px;"/> </div> <div class="buy-table pharmacy"> <div class="buy-table__item"> <div class="buy-table__title"> Адвантан, 0.1%, крем для наружного применения, 15 г, 1 шт. </div> <div class="buy-table__price"> от 600 руб. </div> <div class="buy-table__order"> <a rel="nofollow" href="https://uteka.ru/product/advantan-321287/?utm_source=vidal&amp;utm_medium=cpc&amp;utm_campaign=https://www.vidal.ru/drugs/advantan__8" target="_blank" class="to-ga" data-code="uteka" data-id="207724"> <button class="base-button">Заказать</button> </a> </div> <div class="buy-table__vendor"> Leo Pharma </div> </div> </div> <div style="color: gray; padding: 10px;"> Москва </div> </div> <div> <div id="protec-table" class="buy-header pharmacy-company-vn1"> <span class="buy-header__pharmacy-name">Заказать в аптеке Ваша №1</span> <img src="/upload/photo/header-logo.svg?v21" alt="аптеке Ваша №1" style="max-height: 25px;"/> </div> <div class="buy-table pharmacy"> <div class="buy-table__item"> <div class="buy-table__title"> Адвантан 0,1% 15 г крем для наружного применения </div> <div class="buy-table__price"> 656 руб. </div> <div class="buy-table__order"> <a rel="nofollow" href="https://vn1.ru/product/advantan-krem-d-naruzh-primen-0-1-15g-10026907/?utm_source=vidal&amp;utm_medium=products&amp;utm_campaign=vidal_products_221_10026907" target="_blank" class="to-ga" data-code="vn1" data-id="336372"> <button class="base-button">Заказать</button> </a> </div> <div class="buy-table__vendor"> Bayer HealthCare Manufacturing C.R.P. </div> </div> </div> <div style="color: gray; padding: 10px;"> Москва </div> </div> <i style="display: none" id="regionFound" data-value="Нет"></i> <i style="display: none" id="regionTitle" data-value="Москва"></i> <i style="display: none" id="cityTitle" data-value="Москва"></i> <i style="display: none" id="districtTitle" data-value="Центральный федеральный округ"></i> <i style="display: none" id="regionIp" data-value="176.25.80.24"></i> <!--noindex--> '

    pattern_price = re.compile(r'<div class="buy-table__price">(.*?)</div>')
    pattern_order = re.compile(r'.+ href="(.*?)" target="_blank".+')
    pattern_store = re.compile(r'<span class="buy-header__pharmacy-name">(.*?)</span>')
    match = pattern_price.findall(price_text)
    print(match)
    match = pattern_order.findall(link_text)
    print(match)
    match = pattern_store.findall(text)
    print(match)


def send_scanned_drug_data():
    dm = '010460180801341221myAUS4C56j9RU 91EE08 929NdpsBmbv+9t9+9E/TDNJHm9flmGrIe8AbZ6DYA3SQU='
    #dm = raw_data.split(' ')[0]
    endpoint = 'https://192.168.0.203:8000/add_scanned_drug'
    response = requests.post(f'{endpoint}?dm={dm}', verify=False).json()
    print(response)


def extract_date(date_str: str):
    r = re.findall('(\d{4}-\d{2}-\d{2}).+', date_str)
    if r:
        date_object = datetime.strptime(r[0], "%Y-%m-%d")
        print(r)

if __name__ == '__main__':
    # extract_date('2024-08-01T00:00:00.000Z')
    # mq_test()
    # mq_test_receiver()
    #extract_price_and_link()
    send_scanned_drug_data()
