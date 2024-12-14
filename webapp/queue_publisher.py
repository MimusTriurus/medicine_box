import json
import os

import pika


class QueuePublisher:
    def __init__(self):
        self.connection_params = pika.ConnectionParameters(
            host=os.getenv('RABBITMQ_HOST', default='localhost'),
            port=os.getenv('RABBITMQ_PORT', default=5672),
            virtual_host='/',
            credentials=pika.PlainCredentials(
                username=os.getenv('RABBITMQ_USER', default='guest'),
                password=os.getenv('RABBITMQ_PASS', default='guest')
            )
        )
        self.queue_name = os.getenv('RABBITMQ_QUEUE_NAME', default='medicine_box')

    def qp_put_2_queue(self, data: dict):
        self.connection = pika.BlockingConnection(self.connection_params)
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=self.queue_name, durable=True)

        body_data = json.dumps(data)
        self.channel.basic_publish(
            exchange='',
            routing_key=self.queue_name,
            body=body_data
        )