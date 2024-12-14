import re

DATE_FORMAT = '%Y-%m'

LANG = 'lang'
RU = 'ru'
EN = 'en'

START_DATA = 'start_data'

ICON_SPACER = '  '

# region icons
ICON_CHECK_MARK = u'\U00002705'
ICON_CROSS_MARK = u'\U0000274c'
ICON_PILL = u'\U0001f48a'
ICON_EXPIRED = u'\U000026a0'
ICON_EXCLAMATION = u'\U00002757'
ICON_CALENDAR = u'\U0001F4C5'

ICON_CHARS = u'\U0001f18e'
ICON_NUMS = u'\U0001F522'

ICON_INFO = u'\U00002139'

ICON_TO_LEFT = u'\U000025C0'
ICON_TO_RIGHT = u'\U000025B6'
# endregion

KEY_ID = 'id'
KEY_USER_ID = 'user_id'
KEY_NAME = 'name'
KEY_DATE = 'date'
KEY_LANG = 'lang'
KEY_DRUG_ID = 'drug_id'
KEY_DRUG_DESC = 'description'

KEY_TABLE_USERS = 'users'
KEY_TABLE_AID_KIT = 'non_expired'
KEY_TABLE_AID_KIT_EXPIRED = 'expired'

KEY_TARGET_TABLE = 'target_table'

IDX_ID = 0
IDX_USR_ID = 1
IDX_NAME = 2
IDX_DATE = 3

TABLE_HEIGHT = 6

MSG_NO_INFO = 'No info. Sorry.'

KEY_PRICES = 'prices'
KEY_ORDERS = 'orders'
KEY_IMAGES = 'images'
KEY_STORES = 'stores'

pattern_price = re.compile(r'<div class="buy-table__price">(.*?)</div>')
pattern_order = re.compile(r'.+ href="(.*?)" target="_blank".+')
pattern_store = re.compile(r'<span class="buy-header__pharmacy-name">(.*?)</span>')

pattern_price_html = re.compile(r'<div class="buy-table__price">.*?</div>')
pattern_order_html = re.compile(r'<div class="buy-table__order">.*?</div>')
pattern_img_html = re.compile(r'<img src="/upload.*?/>')

KEY_JAN = 'January'
KEY_FEB = 'February'
KEY_MAR = 'March'
KEY_APR = 'April'
KEY_MAY = 'May'
KEY_JUN = 'June'
KEY_JUL = 'July'
KEY_AUG = 'August'
KEY_SEP = 'September'
KEY_OCT = 'October'
KEY_NOV = 'November'
KEY_DEC = 'December'
KEY_NAME_OF_DRUG = 'name_of_drug'
KEY_NON_EXPIRED = 'non_expired'
KEY_EXPIRED = 'expired'
KEY_DRUG_NOT_AVAILABLE_4_BUY = 'drug_not_available_for_purchase'

EMPTY_DRUG_ID = -1
