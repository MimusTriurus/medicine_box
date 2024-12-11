import gettext

from webapp.constants import (
    EN,
    RU,
    KEY_JAN,
    KEY_FEB,
    KEY_MAR,
    KEY_APR,
    KEY_MAY,
    KEY_JUN,
    KEY_JUL,
    KEY_AUG,
    KEY_SEP,
    KEY_OCT,
    KEY_NOV,
    KEY_DEC,
    KEY_NAME_OF_DRUG,
    KEY_NON_EXPIRED,
    KEY_EXPIRED,
    KEY_DRUG_NOT_AVAILABLE_4_BUY
)

app_name = 'webapp'
localization_dir_name = 'localization'
gettext.bindtextdomain(app_name, f'/{localization_dir_name}')
gettext.textdomain(app_name)

en = gettext.translation(app_name, localedir=localization_dir_name, languages=[EN])
en.install()
ru = gettext.translation(app_name, localedir=localization_dir_name, languages=[RU])
ru.install()

localizers = dict()
localizers[EN] = en
localizers[RU] = ru

_ = gettext.gettext

ID_TXT_JANUARY = _(KEY_JAN)
ID_TXT_FEBRUARY = _(KEY_FEB)
ID_TXT_MARCH = _(KEY_MAR)
ID_TXT_APRIL = _(KEY_APR)
ID_TXT_MAY = _(KEY_MAY)
ID_TXT_JUNE = _(KEY_JUN)
ID_TXT_JULY = _(KEY_JUL)
ID_TXT_AUGUST = _(KEY_AUG)
ID_TXT_SEPTEMBER = _(KEY_SEP)
ID_TXT_OCTOBER = _(KEY_OCT)
ID_TXT_NOVEMBER = _(KEY_NOV)
ID_TXT_DECEMBER = _(KEY_DEC)

ID_TXT_DRUG_NAME = _(KEY_NAME_OF_DRUG)
ID_TXT_NON_EXPIRED = _(KEY_NON_EXPIRED)
ID_TXT_EXPIRED = _(KEY_EXPIRED)
ID_TXT_DRUG_CANT_BUY = _(KEY_DRUG_NOT_AVAILABLE_4_BUY)



