#amqps://zszhwtqp:ohfKwa2VU1nyRmV8BXTPvy_wld7oDQD9@shrimp.rmq.cloudamqp.com/zszhwtqp

import pika

params = pika.URLParameters('amqps://zszhwtqp:ohfKwa2VU1nyRmV8BXTPvy_wld7oDQD9@shrimp.rmq.cloudamqp.com/zszhwtqp')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch,method, properties, body):
    print('Received in admin')
    print(body)

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()