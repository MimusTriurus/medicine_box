import os

TOKEN = os.getenv('BOT_TOKEN')

# region webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', default='https://medicine-box-bot.onrender.com')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', default='')
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
# endregion

# region webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=80)
DB_URL = os.getenv('DATABASE_URL', default='sqlite:///drugs.db')
# endregion
