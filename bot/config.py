import os

TOKEN = os.getenv('BOT_TOKEN')
DB_URL = os.getenv('DATABASE_URL', default='sqlite:///db/medicine_boxes.db')
