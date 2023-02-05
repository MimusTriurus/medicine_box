from constants import *
from localization.localization_keys import *


def make_add_btn_title(lang_code: str) -> str:
    return f'{ICON_CHECK_MARK}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_ADD)}'


def make_del_btn_title(lang_code: str) -> str:
    return f'{ICON_CROSS_MARK}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_DEL)}'


def make_actual_btn_title(lang_code: str) -> str:
    return f'{ICON_PILL}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_VIEW_ACTUAL)}'


def make_expired_btn_title(lang_code: str) -> str:
    return f'{ICON_EXPIRED}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_VIEW_EXPIRED)}'


def make_cancel_btn_title(lang_code: str) -> str:
    return f'{ICON_CROSS_MARK}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_CANCEL)}'


def make_clean_btn_title(lang_code: str) -> str:
    return f'{ICON_CROSS_MARK}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_CLEAN)}'

def make_start_message(lang_code: str) -> str:
    localizer = localizers.get(lang_code, en)
    hello_message = localizer.gettext(ID_START) + '\n\n'
    hello_message += f'{localizer.gettext(ID_PRESS_ADD_BTN)} ' \
                     f'<b>{make_add_btn_title(lang_code)}</b>' \
                     f'{localizer.gettext(ID_TO_ADD_DRUG)}'
    return hello_message


def make_add_drug_name_message(lang_code: str) -> str:
    return f'{ICON_CHARS}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_TXT_DRUG_NAME_INPUT)}'


def make_add_drug_date_message(lang_code: str) -> str:
    return f'{ICON_CALENDAR}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_TXT_DRUG_DATE_INPUT)}'


def make_error_on_set_date_message(lang_code: str) -> str:
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_TXT_ERROR_DATE)}'


def make_drug_is_expired_message(lang_code: str, drug_name: str, drug_expired_date) -> str:
    return f'{ICON_EXPIRED}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_TXT_TIME_IS_OVER)}:' \
           f' <b>{drug_name} {drug_expired_date}</b>'


def make_4_del_drugs_table_message(lang_code: str, table_str: str) -> str:
    res = f'{ICON_PILL}{ICON_SPACER}<b>{localizers.get(lang_code, en).gettext(ID_TITLE_ACTUAL_DRUGS)}:</b>\n'
    res += '<pre>\n</pre>'
    res += f'{table_str}'
    res += '<pre>\n</pre>'
    res += f'{localizers.get(lang_code, en).gettext(ID_TITLE_INPUT_DRUGS_4_DELETE)}'
    return res


def make_drugs_table_message(lang_code: str, table_str: str) -> str:
    res = f'{ICON_PILL}{ICON_SPACER}<b>{localizers.get(lang_code, en).gettext(ID_TITLE_ACTUAL_DRUGS)}:</b>\n'
    res += '<pre>\n</pre>'
    res += f'{table_str}'
    return res


def make_expired_drugs_table_message(lang_code: str, table_str: str) -> str:
    res = f'{ICON_EXPIRED}{ICON_SPACER}<b>{localizers.get(lang_code, en).gettext(ID_TITLE_EXPIRED_DRUGS)}:</b>\n'
    res += '<pre>\n</pre>'
    res += f'{table_str}'
    return res


def make_first_aid_kit_is_empty_message(lang_code: str):
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_TXT_FIRST_AID_KIT_IS_EMPTY)}'


def make_expired_drugs_lst_is_empty_message(lang_code: str):
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_TXT_EXPIRED_DRUGS_NOT_FOUND)}'


def make_cancelled_message(lang_code: str):
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_CANCELLED)}'


def make_done_message(lang_code: str) -> str:
    return f'{ICON_CHECK_MARK}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_DONE)}'


def make_drug_added_message(lang_code: str, drug_name: str, drug_expired_date) -> str:
    return f'{ICON_CHECK_MARK}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_ADDED)}:' \
           f' <b>{drug_name} {drug_expired_date}</b>'


def make_drug_deleted_message(lang_code: str, drug_name: str, drug_expired_date) -> str:
    return f'{ICON_CHECK_MARK}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_DELETED)}:' \
           f' <b>{drug_name} {drug_expired_date}</b>'


def make_drug_not_found_message(lang_code: str, drug_id: str) -> str:
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{localizers.get(lang_code, en).gettext(ID_NOT_FOUND)}. ID: <b>{drug_id}</b>'


def make_drug_deleted_message(lang_code: str, drug_title: str) -> str:
    return f'{localizers.get(lang_code, en).gettext(ID_TXT_REMOVED)}: {drug_title}'


def make_actual_drugs_table_title(lang_code: str):
    return localizers.get(lang_code, en).gettext(ID_TXT_ACTUAL_DRUGS)


def make_del_actual_drugs_table_title(lang_code: str):
    return localizers.get(lang_code, en).gettext(ID_TXT_DEL_ACT_DRUGS)


def make_expired_drugs_table_title(lang_code: str):
    return localizers.get(lang_code, en).gettext(ID_TXT_EXP_DRUGS)


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
