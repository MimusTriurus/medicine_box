from constants import *
from localization.ru import ru_strings
from localization.localization_keys import *

localization = dict()
localization[RU] = ru_strings


def get_strings_dict(lang_code: str) -> dict:
    strings = None
    if lang_code not in localization.keys():
        strings = localization[RU]
    else:
        strings = localization[lang_code]
    return strings


def make_add_btn_title(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_CHECK_MARK}{ICON_SPACER}{strings[ID_ADD]}'


def make_del_btn_title(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_CROSS_MARK}{ICON_SPACER}{strings[ID_DEL]}'


def make_actual_btn_title(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_PILL}{ICON_SPACER}{strings[ID_VIEW_ACTUAL]}'


def make_expired_btn_title(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_EXPIRED}{ICON_SPACER}{strings[ID_VIEW_EXPIRED]}'


def make_cancel_btn_title(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_CROSS_MARK}{ICON_SPACER}{strings[ID_CANCEL]}'


def make_clean_btn_title(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_CROSS_MARK}{ICON_SPACER}{strings[ID_CLEAN]}'


def make_start_message(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return strings[ID_START]


def make_add_drug_name_message(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_CHARS}{ICON_SPACER}{strings[ID_TXT_DRUG_NAME_INPUT]}'


def make_add_drug_date_message(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_CALENDAR}{ICON_SPACER}{strings[ID_TXT_DRUG_DATE_INPUT]}'


def make_error_on_set_date_message(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{strings[ID_TXT_ERROR_DATE]}'


def make_drug_is_expired_message(lang_code: str, drug_name: str, drug_expired_date) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_EXPIRED}{ICON_SPACER}{strings[ID_TXT_TIME_IS_OVER]}: <b>{drug_name} {drug_expired_date}</b>'


def make_4_del_drugs_table_message(lang_code: str, table_str: str) -> str:
    strings = get_strings_dict(lang_code)
    res = f'{ICON_PILL}{ICON_SPACER}<b>{strings[ID_TITLE_ACTUAL_DRUGS]}:</b>\n'
    res += '<pre>\n</pre>'
    res += f'{table_str}'
    res += '<pre>\n</pre>'
    res += f'{strings[ID_TITLE_INPUT_DRUGS_4_DELETE]}'
    return res


def make_drugs_table_message(lang_code: str, table_str: str) -> str:
    strings = get_strings_dict(lang_code)
    res = f'{ICON_PILL}{ICON_SPACER}<b>{strings[ID_TITLE_ACTUAL_DRUGS]}:</b>\n'
    res += '<pre>\n</pre>'
    res += f'{table_str}'
    return res


def make_expired_drugs_table_message(lang_code: str, table_str: str) -> str:
    strings = get_strings_dict(lang_code)
    res = f'{ICON_EXPIRED}{ICON_SPACER}<b>{strings[ID_TITLE_EXPIRED_DRUGS]}:</b>\n'
    res += '<pre>\n</pre>'
    res += f'{table_str}'
    return res


def make_first_aid_kit_is_empty_message(lang_code: str):
    strings = get_strings_dict(lang_code)
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{strings[ID_TXT_FIRST_AID_KIT_IS_EMPTY]}'


def make_expired_drugs_lst_is_empty_message(lang_code: str):
    strings = get_strings_dict(lang_code)
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{strings[ID_TXT_EXPIRED_DRUGS_NOT_FOUND]}'


def make_cancelled_message(lang_code: str):
    strings = get_strings_dict(lang_code)
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{strings[ID_CANCELLED]}'


def make_done_message(lang_code: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_CHECK_MARK}{ICON_SPACER}{strings[ID_DONE]}'


def make_drug_added_message(lang_code: str, drug_name: str, drug_expired_date) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_CHECK_MARK}{ICON_SPACER}{strings[ID_ADDED]}: <b>{drug_name} {drug_expired_date}</b>'


def make_drug_deleted_message(lang_code: str, drug_name: str, drug_expired_date) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_CHECK_MARK}{ICON_SPACER}{strings[ID_DELETED]}: <b>{drug_name} {drug_expired_date}</b>'


def make_drug_not_found_message(lang_code: str, drug_id: str) -> str:
    strings = get_strings_dict(lang_code)
    return f'{ICON_EXCLAMATION}{ICON_SPACER}{strings[ID_NOT_FOUND]}. ID: <b>{drug_id}</b>'
