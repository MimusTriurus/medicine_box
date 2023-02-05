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
ID_ADD = _('ADD')
ID_DEL = _('DEL')
ID_ADDED = _('ADDED')
ID_DELETED = _('DELETED')
ID_VIEW_ACTUAL = _('VIEW_ACTUAL')
ID_VIEW_EXPIRED = _('VIEW_EXPIRED')
ID_CLEAR_EXPIRED = _('CLEAR_EXPIRED')
ID_CANCEL = _('CANCEL')
ID_CANCELLED = _('CANCELLED')
ID_CLEAN = _('CLEAN')
ID_DONE = _('DONE')
ID_NOT_FOUND = _('NOT_FOUND')

ID_TITLE_ACTUAL_DRUGS = _('TITLE_ACTUAL_DRUGS')
ID_TITLE_EXPIRED_DRUGS = _('TITLE_EXPIRED_DRUGS')
ID_TITLE_INPUT_DRUGS_4_DELETE = _('TITLE_INPUT_DRUGS_4_DELETE')

ID_TXT_DRUG_NAME_INPUT = _('TXT_DRUG_NAME_INPUT')

ID_TXT_DRUG_DATE_INPUT = _('TXT_DRUG_DATE_INPUT')

ID_TXT_ERROR_DATE = _('TXT_ERROR_DATE')
ID_TXT_TIME_IS_OVER = _('TXT_TIME_IS_OVER')

ID_TXT_FIRST_AID_KIT_IS_EMPTY = _('TXT_FIRST_AID_KIT_IS_EMPTY')
ID_TXT_EXPIRED_DRUGS_NOT_FOUND = _('TXT_EXPIRED_DRUGS_NOT_FOUND')

ID_TXT_REMOVED = _('Removed: ')
ID_TXT_ACTUAL_DRUGS = _('Actual drugs')
ID_TXT_DEL_ACT_DRUGS = _('Delete actual drugs')
ID_TXT_EXP_DRUGS = _('Expired drugs')

ID_TXT_SELECT_YEAR = _('Select year')
ID_TXT_YEAR = _('Year')

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
