import os
import pika
import json

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main1.settings")  # Replace 'yourproject' with your Django project name

import django

django.setup()

from products.models import Product

params = pika.URLParameters('amqps://zszhwtqp:ohfKwa2VU1nyRmV8BXTPvy_wld7oDQD9@shrimp.rmq.cloudamqp.com/zszhwtqp')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='main1')

def callback(ch, method, properties, body):
    print('Received in main1')
    data = json.loads(body.decode('utf-8'))  # Ensure the body is loaded as a dictionary
    print(data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        product.save()
        print('Product saved')
        print('Product created')

    elif properties.content_type == 'product_updated':
        product = Product.objects.get(id=data['id'])
        product.title = data['title']
        product.image = data['image']
        product.save()
        print('Product updated')

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