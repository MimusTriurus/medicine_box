import os

TOKEN = os.getenv('BOT_TOKEN')
DB_URL = os.getenv('DATABASE_URL', default='sqlite:///medicine_boxes.db')
DRUGS_DB_URL = os.getenv('DRUGS_DB_URL', default='sqlite:///drugs.db')
WEBAPP_PORT = int(os.getenv('WEBAPP_PORT', default=8000))
