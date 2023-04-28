import pika
import mysql.connector
import json

credentials = pika.PlainCredentials('guest', 'guest')
connection = pika.BlockingConnection(pika.ConnectionParameters('10.20.202.64', 5672, '/', credentials))

channel = connection.channel()
channel.exchange_declare(exchange='insertion', exchange_type='direct')
channel.queue_declare(queue='insertion_queue')
channel.queue_bind(exchange='insertion', queue='insertion_queue')

mydb = mysql.connector.connect(
    host='mysql',
    user="root",
    database="student_records",
    password="root"
)
c = mydb.cursor()

def callback(ch, method, properties, body):
    data = json.loads(body)
    print("Received message for inserting record: {}".format(data))
    # insert the record into the database
    c.execute("INSERT INTO students_info (name, srn, section) VALUES (%s, %s, %s)", (data["name"], data["srn"], data["section"]))
    mydb.commit()
    # acknowledge that the message has been received
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_consume(queue='insertion_queue', on_message_callback=callback)
channel.start_consuming()


