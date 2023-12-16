#amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo
import os
import pika
import json

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")  # Replace 'yourproject' with your Django project name

import django

django.setup()

from product.models import Product


params = pika.URLParameters('amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='admin')

def callback(ch,method, properties, body):
    print('Received in admin')
    data = json.loads(body.decode('utf-8'))  # Ensure the body is loaded as a dictionary
    print(body)

    if properties.content_type == 'product_updated':
        product = Product.objects.get(id=data['id'])
        product.title = data['title']
        product.image = data['image']
        product.likes = data['likes']
        product.save()
        print('Product updated')

channel.basic_consume(queue='admin', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()