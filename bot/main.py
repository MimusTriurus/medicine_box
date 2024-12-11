import logging
import os

import pika

from aiogram import Dispatcher
from aiogram.utils.executor import start_polling
from pika import BlockingConnection
from pika.adapters.asyncio_connection import AsyncioConnection

from db_management import sql_start, sql_stop
from expired_drugs_checker import scheduler, check_expired_drugs_queue
from handlers import *

logging.basicConfig(level=logging.INFO)
log = logging.getLogger()


async def check():
    connection_params = pika.ConnectionParameters(
        host='localhost',
        port=5672,
        virtual_host='/',
        credentials=pika.PlainCredentials(
            username='guest',
            password='guest'
        )
    )

    connection = AsyncioConnection(connection_params)
    connection.ioloop.run_forever()
    channel = await connection.channel()

    queue_name = 'hello'

    def callback(ch, method, properties, body):
        print(f"Received: '{body}'")

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True
    )

    print('Waiting for messages. To exit, press Ctrl+C')
    channel.start_consuming()


async def on_startup(dispatcher: Dispatcher):
    log.info('bot started...')
    await sql_start()

    connection_params = pika.ConnectionParameters(
        host=os.getenv('RABBITMQ_HOST', default='localhost'),
        port=os.getenv('RABBITMQ_PORT', default=5672),
        virtual_host='/',
        credentials=pika.PlainCredentials(
            username=os.getenv('RABBITMQ_USER', default='guest'),
            password=os.getenv('RABBITMQ_PASS', default='guest')
        )
    )
    connection = BlockingConnection(connection_params)
    scheduler.add_job(check_expired_drugs_queue, 'interval', seconds=10, args=(dispatcher, connection.channel(), ))
    scheduler.start()

    dispatcher.register_message_handler(request_start_handler)


def bot_start_polling():
    start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)


async def on_shutdown(dispatcher: Dispatcher):
    log.info('bot stopped...')
    await sql_stop()


def main():
    bot_start_polling()
    return 0


if __name__ == '__main__':
    exit(main())
