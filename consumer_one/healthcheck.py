import pika
import time

while True:
    try:
        #connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        connection.channel()
        connection.close()
        print('RabbitMQ is up and running!')
        break
    except pika.exceptions.AMQPConnectionError:
        print('RabbitMQ not available. Retrying in 5 seconds...')
        time.sleep(5)

