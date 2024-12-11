from localization_keys import *


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
