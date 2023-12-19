#amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo
import os
import pika
import json
from django.db import OperationalError
import time

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "admin.settings")  # Replace 'yourproject' with your Django project name

import django

django.setup()

from product.models import Product


params = pika.URLParameters('amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo')

connection = pika.BlockingConnection(params)

channel = connection.channel()

channel.queue_declare(queue='temp')

def callback(ch,method, properties, body):
    print('Received in admin')
    data = json.loads(body.decode('utf-8'))  # Ensure the body is loaded as a dictionary
    print(body)

    # Attempt to connect to the database with retry logic
    retry_count = 0
    max_retries = 3

    while retry_count < max_retries:
        try:
            # Your database operations here
            # For example: YourModel.objects.create(**product_data)

         if properties.content_type == 'product_updated':
          product = Product.objects.get(id=data['id'])
        #   product.title = data['title']
        #   product.image = data['image']
          product.likes = data['likes']
          product.save()
          print('Product updated')
          break
       
        except OperationalError as e:
            print(f"Database connection error: {e}")
            print(f"Retrying ({retry_count + 1}/{max_retries})...")
            retry_count += 1
            time.sleep(2 ** retry_count)  # Backoff strategy

    if retry_count == max_retries:
        print("Max retries reached. Unable to connect to the database.")




channel.basic_consume(queue='temp', on_message_callback=callback, auto_ack=True)

print('Started Consuming')

channel.start_consuming()

channel.close()