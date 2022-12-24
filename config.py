import os

TOKEN = os.getenv('BOT_TOKEN', default='5672940238:AAGZdIiqJ2s7pSM7t6qzLR4g0Lj50VBRWsg')
HEROKU_APP_NAME = os.getenv('HEROKU_APP_NAME', default='medicine_box')

# region webhook settings
WEBHOOK_HOST = f'https://{HEROKU_APP_NAME}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
# endregion

# region webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)
DB_URL = os.getenv('DATABASE_URL', default='sqlite:///drugs.db')
# endregion

IS_LOCAL_MODE = os.getenv('IS_LOCAL_MODE', default=True)
