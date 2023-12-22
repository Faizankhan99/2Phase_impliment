#amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo

import pika, json,requests

MAIN_MICROSERVICE_URL = "http://docker.for.win.localhost:8000/api/product" 


def is_main_microservice_active():
    try:
        print('response-->')
        response = requests.get('http://192.168.29.45:8003/api/test')
        print('response-->',response)
        if(response.status_code == 200):
            print("Krishna")
            return True
    except requests.RequestException as e:
        print(f'response-->',e)
        return False
    

        # In-memory storage for temporary data
temporary_storage = []
print("temporary_storage-->",temporary_storage)


params = pika.URLParameters('amqps://vmsvqzzo:BYr7CpyY2QS-0pUusXMHpWuPe1pyOyXQ@octopus.rmq3.cloudamqp.com/vmsvqzzo')

connection = pika.BlockingConnection(params)

channel = connection.channel()

def publish(method, body):
      if is_main_microservice_active():
        # Main microservice is active, publish the message
        print("method, body----->", method, body)
        properties = pika.BasicProperties(method) 
        channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
        return True
      else:
        # Main microservice is not active, store data temporarily
        print(f"Main microservice is not active. Storing message temporarily: {method}, {body}")
        temporary_storage.append((method, body))
        return False
        # Implement additional logic as needed  
    # print('method,body from main1----->',method,body)
    # properties = pika.BasicProperties(method) 
    # print('properties----->',properties)
    # channel.basic_publish(exchange='',routing_key='admin', body=json.dumps(body), properties=properties)
     

