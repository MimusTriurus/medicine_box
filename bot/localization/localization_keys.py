import gettext

from constants import EN, RU

app_name = 'bot'
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

ID_START = _('START')
ID_PRESS_ADD_BTN = _('PRESS_ADD_BTN')
ID_TO_ADD_DRUG = _('TO_ADD_DRUG')

ID_TXT_JANUARY = _('January')
ID_TXT_FEBRUARY = _('February')
ID_TXT_MARCH = _('March')
ID_TXT_APRIL = _('April')
ID_TXT_MAY = _('May')
ID_TXT_JUNE = _('June')
ID_TXT_JULY = _('July')
ID_TXT_AUGUST = _('August')
ID_TXT_SEPTEMBER = _('September')
ID_TXT_OCTOBER = _('October')
ID_TXT_NOVEMBER = _('November')
ID_TXT_DECEMBER = _('December')

ID_MEDICATION = _('The medication')
ID_EXPIRED_IN = _('expired in')

FAK_BTN_TITLE = _('FAK_BTN_TITLE')

BUY_BTN_TITLE = _('BUY_BTN_TITLE')
