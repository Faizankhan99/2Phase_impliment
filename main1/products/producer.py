#amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo

import pika, json

params = pika.URLParameters('amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
    print('method,body from main1----->',method,body)
    properties = pika.BasicProperties(method) 
    print('properties----->',properties)
    channel.basic_publish(exchange='',routing_key='admin', body=json.dumps(body), properties=properties)