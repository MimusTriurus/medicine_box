import os

DRUGS_DB_URL = os.getenv('DRUGS_DB_URL', default='sqlite:///db/drugs.db')
WEBAPP_PORT = int(os.getenv('WEBAPP_PORT', default=8000))
WEBAPP_DOMAIN = os.getenv('BASE_DOMAIN')

IS_IT_PROD = os.getenv('IS_IT_PROD', default=False)

PASSWORD = os.getenv('PASSWORD')
