import os

DRUGS_DB_URL = os.getenv('DRUGS_DB_URL', default='sqlite:///db/drugs.db')
DB_URL = os.getenv('DATABASE_URL', default='sqlite:///db/medicine_boxes.db')
WEBAPP_PORT: int = int(os.getenv('WEBAPP_PORT', default=8000))
VIDAL_LINK = os.getenv('VIDAL_LINK', default='https://www.vidal.ru')
