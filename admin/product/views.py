from django.shortcuts import render
from django.db import OperationalError


from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User
from .producer import publish
from .serializers import ProductSerializer
import random 
temporary_storage = []

import time
import requests
temporary_storage=[]

def is_main_microservice_active():
    try:
        print('response of main-->')
        response = requests.get('http://192.168.29.45:8002/api/products')
        print('response of main-->',response)
        if(response.status_code == 200):
            print("Krishna")
            return True
    except requests.RequestException as e:
        print(f'response-->',e)
        return False





def check_admin_active(content,self, request, pk=None):
    retry_count = 0
    max_retries = 3
    while retry_count < max_retries:
          try:
             if temporary_storage:
                 if is_main_microservice_active():
                  print("Hello")
                  if(content == "product_created"):
                       serializer = ProductSerializer(data=request.data)
                       serializer.is_valid(raise_exception=True)
                       serializer.save()
                       print("serializer.data----->",serializer.data)
                       publish('product_created', serializer.data)
                  elif(content == "product_deleted"):
                       product = Product.objects.get(id=pk)
                       product.delete()
                       publish('product_deleted', pk)
                  else:    
                     product = Product.objects.get(id=pk)
                     print("Product-->",product)
                     serializer = ProductSerializer(instance=product, data=request.data)
                     print("Product-->",serializer)
                     serializer.is_valid(raise_exception=True)
                     serializer.save()
                     publish(content, serializer.data)
                  break
          except OperationalError as e:
            print(f"Database connection error: {e}")
            print(f"Retrying ({retry_count + 1}/{max_retries})...")
            retry_count += 1
            time.sleep(2 ** retry_count)  # Backoff strategy
    if retry_count == max_retries:
        print("Max retries reached. Unable to connect to the database.")
 





# Create your views here.
def get_serializer_class(self):
    return self


#   def list(self, *args, **kwargs):
#         self.serializer_class = self.list_serializer
#         return viewsets.ModelViewSet.list(self, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        return ProductSerializer
       
    def list(self, request): # /api/product
        product = self.get_queryset() 
        serializer = ProductSerializer(product, many=True)
        # publish('product_c', serializer.data)
        return Response(serializer.data)

    def create(self, request): # /api/product
        serializer = ProductSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if is_main_microservice_active():
           serializer.save() 
           print("serializer-->",serializer)
           publish('product_created', serializer.data)
        else:
            temporary_storage.append(serializer.data)
            print("temporary_storage--->",temporary_storage)
            check_admin_active("product_created",self, request)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def retrieve(self, request, pk=None): # /api/product/<str:id>
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None): # /api/product/<str:id>
        product = Product.objects.get(id=pk)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
           # Store validated data before calling save
        validated_data = serializer.validated_data
        validated_data['id'] = pk 
        temporary_storage.append(validated_data)
        print("validated_data -->",validated_data )
        # publish('product_updated', validated_data)
        if publish('product_updated', validated_data):
         serializer.save()
        else:
            temporary_storage.append(validated_data)
            check_admin_active('product_updated',self, request, pk)
            print("temporary_storage--->",temporary_storage)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None): # /api/product/<str:id>
        product = Product.objects.get(id=pk)
        if publish('product_deleted', pk):
           product.delete()
           publish('product_deleted', pk)
        else:
            temporary_storage.append(pk)
            check_admin_active('product_deleted',self, request, pk)
            print("temporary_storage--->",temporary_storage)
   
        return Response(status=status.HTTP_204_NO_CONTENT)

    

class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })
