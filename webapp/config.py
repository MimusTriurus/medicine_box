import os

DRUGS_DB_URL = os.getenv('DRUGS_DB_URL', default='sqlite:///db/drugs.db')
DB_URL = os.getenv('DATABASE_URL', default='sqlite:///db/medicine_boxes.db')
WEBAPP_PORT: int = int(os.getenv('WEBAPP_PORT', default=8000))
IS_IT_PROD: bool = bool(int(os.getenv('IS_IT_PROD', default=True)))
