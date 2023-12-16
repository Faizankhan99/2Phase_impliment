#amqps://zszhwtqp:ohfKwa2VU1nyRmV8BXTPvy_wld7oDQD9@shrimp.rmq.cloudamqp.com/zszhwtqp
import pika,json

#import os
#os.chdir('D:\\Reserch project\\MyApp\\main1')

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from .main1.products.models import Products


params = pika.URLParameters('amqps://zszhwtqp:ohfKwa2VU1nyRmV8BXTPvy_wld7oDQD9@shrimp.rmq.cloudamqp.com/zszhwtqp')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main1')

def callback(ch,method, properties, body):
    print('Received in main1')
    data = json.loads(body)
    print(data)


    if properties['content_type'] == 'product_created':
        product = Products(id=data['id'], title=data['title'], image=data['image'])
        product.save()

    elif properties['content_type'] == 'product_updated':
        product = Products.objects.get(id=data['id'])
        product.title = data['title']
        product.image = data['image']
        product.save()

    elif properties['content_type'] == 'product_deleted':
        try:
            product = Products.objects.get(id=data['id'])
            product.delete()
        except Products.DoesNotExist:
        # Handle the case where the product does not exist
            pass  

channel.basic_consume(queue='main1', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()