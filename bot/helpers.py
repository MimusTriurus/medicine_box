from datetime import datetime
from constants import DATE_FORMAT


def time_is_over(date_str: str) -> bool:
    date = datetime.strptime(date_str, DATE_FORMAT)
    current_date = datetime.now()
    return current_date >= date

