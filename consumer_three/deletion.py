import pika
import json
from pymongo import MongoClient


client = MongoClient('mongodb://mongo:27017/')
db = client['student_management']
collection = db['students']


def callback(ch, method, properties, body):
    message = json.loads(body)
    if 'SRN' in message and 'action' in message and message['action'] == 'delete':
        collection.delete_one({'SRN': message['SRN']})
        print(f'Student {message["SRN"]} deleted successfully!')
    else:
        print('Invalid delete request!')


connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
