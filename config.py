import os

TOKEN = os.getenv('BOT_TOKEN', default='5533694427:AAFO6SvorZxHT88dQI2TVETdZ1wZjDH4BxU')

# region webhook settings
WEBHOOK_HOST = os.getenv('WEBHOOK_HOST', default='https://medicine-box-bot.onrender.com')
WEBHOOK_PATH = os.getenv('WEBHOOK_PATH', default='/')
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
# endregion

# region webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8443)
DB_URL = os.getenv('DATABASE_URL', default='sqlite:///drugs.db')
# endregion
