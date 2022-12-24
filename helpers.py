from datetime import datetime

from tabulate import tabulate

from constants import *


def time_is_over(date_str: str) -> bool:
    date = datetime.strptime(date_str, DATE_FORMAT)
    current_date = datetime.now()
    # return False
    return current_date > date


def validate_date(date_str: str) -> bool:
    try:
        datetime.strptime(date_str, DATE_FORMAT)
        return True
    except ValueError:
        return False


def make_table_str(items, with_id: bool = False):
    head = ['Id', 'Title', 'Date'] if with_id else ['Title', 'Date']
    data = list()
    for item in items:
        record = [item[KEY_ID], item[KEY_NAME], item[KEY_DATE]] if with_id else [item[KEY_NAME], item[KEY_DATE]]
        data.append(record)
    return f'<pre>{tabulate(data, headers=head, tablefmt="grid")}</pre>'


def make_expired_drug_message(drug):
    return f'Drug {drug[2]} is expired in {drug[3]}'
