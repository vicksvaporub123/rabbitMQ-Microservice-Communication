import pika
import json
from pymongo import MongoClient
from flask import Flask, jsonify


client = MongoClient('mongodb://mongo:27017/')
db = client['student_management']
collection = db['students']


app = Flask(__name__)


@app.route('/students')
def get_students():
    students = []
    for student in collection.find():
        student.pop('_id')
        students.append(student)
    return jsonify(students)


connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='student')


def callback(ch, method, properties, body):
    message = json.loads(body)
    if 'SRN' in message and 'name' in message and 'branch' in message:
        collection.insert_one(message)
        print(f'Student {message["SRN"]} inserted successfully!')
    elif 'SRN' in message and 'action' in message and message['action'] == 'delete':
        collection.delete_one({'SRN': message['SRN']})
        print(f'Student {message["SRN"]} deleted successfully!')
    else:
        print('Invalid message format!')


channel.basic_consume(queue='student', on_message_callback=callback, auto_ack=True)
channel.start_consuming()


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
