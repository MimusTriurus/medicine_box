from constants import *
from localization.localization_keys import *


def make_start_message(lang_code: str) -> str:
    localizer = localizers.get(lang_code, en)
    hello_message = localizer.gettext(ID_START) + '\n\n'
    hello_message += f'{localizer.gettext(ID_PRESS_ADD_BTN)} ' \
                     f'<b>•••</b> ' \
                     f'{localizer.gettext(ID_TO_ADD_DRUG)}'
    return hello_message


def make_first_aid_kit_examble_btn_title(lang_code: str) -> str:
    localizer = localizers.get(lang_code, en)
    btn_title = localizer.gettext(FAK_BTN_TITLE)
    return btn_title


def make_buy_drug_btn_title(lang_code: str) -> str:
    localizer = localizers.get(lang_code, en)
    btn_title = localizer.gettext(BUY_BTN_TITLE)
    return btn_title


def make_month_title(month_number: int, lang_code: str):
    loc = localizers.get(lang_code, en)
    months = {
        1: loc.gettext(ID_TXT_JANUARY),
        2: loc.gettext(ID_TXT_FEBRUARY),
        3: loc.gettext(ID_TXT_MARCH),
        4: loc.gettext(ID_TXT_APRIL),
        5: loc.gettext(ID_TXT_MAY),
        6: loc.gettext(ID_TXT_JUNE),
        7: loc.gettext(ID_TXT_JULY),
        8: loc.gettext(ID_TXT_AUGUST),
        9: loc.gettext(ID_TXT_SEPTEMBER),
        10: loc.gettext(ID_TXT_OCTOBER),
        11: loc.gettext(ID_TXT_NOVEMBER),
        12: loc.gettext(ID_TXT_DECEMBER),
    }

    return months[month_number]


def make_expired_drug_message(lang_code: str, drug_name: str, drug_expired_date: str):
    date_parts = drug_expired_date.split('-')
    year = ''
    month = drug_expired_date
    if len(date_parts) == 2:
        year = date_parts[0]
        month_num = int(date_parts[1])
        month = make_month_title(month_num, lang_code)

    return (
        f'{ICON_EXCLAMATION}{ICON_SPACER}'
        f'{localizers.get(lang_code, en).gettext(ID_MEDICATION)} '
        f'<b>{drug_name}</b> '
        f'{localizers.get(lang_code, en).gettext(ID_EXPIRED_IN)} '
        f'<b>{month} {year}</b>'
    )
