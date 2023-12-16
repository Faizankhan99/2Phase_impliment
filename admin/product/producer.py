#amqps://zszhwtqp:ohfKwa2VU1nyRmV8BXTPvy_wld7oDQD9@shrimp.rmq.cloudamqp.com/zszhwtqp

import pika, json

params = pika.URLParameters('amqps://zszhwtqp:ohfKwa2VU1nyRmV8BXTPvy_wld7oDQD9@shrimp.rmq.cloudamqp.com/zszhwtqp')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    properties = pika.BasicProperties(method) 
    channel.basic_publish(exchange='',routing_key='main1', body=json.dumps(body), properties=properties)