import pika
import json
from flask import Flask, request, jsonify


app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='student')


@app.route('/')
def index():
    return "Student Management System is up and running!"


@app.route('/health')
def health_check():
    
    status = {'status': 'OK'}
    return jsonify(status)


@app.route('/students', methods=['GET', 'POST'])
def students():
    if request.method == 'GET':
        response = channel.basic_get(queue='student', auto_ack=True)
        if response is not None:
            message = json.loads(response.body)
            return jsonify(message)
        else:
            return jsonify({'message': 'No students found!'})
    elif request.method == 'POST':
        data = request.json
        channel.basic_publish(exchange='', routing_key='student', body=json.dumps(data))
        return jsonify({'message': 'Student added successfully!'})


@app.route('/students/<srn>', methods=['DELETE'])
def delete_student(srn):
    channel.basic_publish(exchange='', routing_key='student', body=json.dumps({'SRN': srn, 'action': 'delete'}))
    return jsonify({'message': 'Student deleted successfully!'})


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
