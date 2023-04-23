import pika
import json
from pymongo import MongoClient


client = MongoClient('mongodb://mongo:27017/')
db = client['student_management']
collection = db['students']


def callback(ch, method, properties, body):
    message = json.loads(body)
    if 'SRN' in message and 'name' in message and 'branch' in message:
        collection.insert_one(message)
        print(f'Student {message["SRN"]} inserted successfully!')
    else:
        print('Invalid student data!')


connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='student')
channel.basic_consume(queue='student', on_message_callback=callback, auto_ack=True)
channel.start_consuming()