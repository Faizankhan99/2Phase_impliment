#amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo
import pika,json

#import os
#os.chdir('D:\\Reserch project\\MyApp\\main1')

import sys
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(SCRIPT_DIR))

from .main1.products.models import Products


params = pika.URLParameters('amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo')

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

    elif properties.content_type == 'product_deleted':
        if isinstance(data, dict):
            product_id = data.get('id')
            if product_id is not None:
                try:
                    product = Product.objects.get(id=product_id)
                    product.delete()
                    print('Product deleted')
                except Product.DoesNotExist as e:
                    print(f"Error: Product with ID {product_id} does not exist. {e}")
            else:
                print("Error: 'id' key not found in data or is None")
        else:
            print("Error: Invalid data format, expected a dictionary")

channel.basic_consume(queue='main1', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()