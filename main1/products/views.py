from django.shortcuts import render
from django.db import OperationalError

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product,User
from .producer import publish
from .serializers import ProductSerializer
import random 
import time
import requests
temporary_storage=[]

def is_main_microservice_active():
    try:
        print('response of main-->')
        response = requests.get('http://192.168.135.232:8003/api/test')
        print('response of main-->',response)
        if(response.status_code == 200):
            print("Krishna")
            return True
    except requests.RequestException as e:
        print(f'response-->',e)
        return False


def check_admin_active(self, request, pk):
    retry_count = 0
    max_retries = 3
    while retry_count < max_retries:
          try:
             if temporary_storage:
                 if is_main_microservice_active():
                  product = Product.objects.get(id=pk)
                  print("Product-->",product)
                  serializer = ProductSerializer(instance=product, data=request.data)
                  print("Product-->",serializer)
                  serializer.is_valid(raise_exception=True)
                #   validated_data = serializer.validated_data
                #   validated_data['id'] = pk 
                  serializer.save()
                  publish('product_updated', serializer.data)
                  break
          except OperationalError as e:
            print(f"Database connection error: {e}")
            print(f"Retrying ({retry_count + 1}/{max_retries})...")
            retry_count += 1
            time.sleep(2 ** retry_count)  # Backoff strategy
    if retry_count == max_retries:
        print("Max retries reached. Unable to connect to the database.")
 


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    def get_serializer_class(self):
        return ProductSerializer
       
    def list(self, request): # /api/product
        product = self.get_queryset() 
        serializer = ProductSerializer(product, many=True)
        # publish('product_c', serializer.data)
        return Response(serializer.data)

    def retrieve(self, request, pk=None): # /api/product/<str:id>
        product = Product.objects.get(id=pk)
        print("product-->",product)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None): # /api/product/<str:id>
        product = Product.objects.get(id=pk)
        print("product--->",product.likes)
        serializer = ProductSerializer(instance=product, data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        validated_data['id'] = pk 
        if publish('product_updated', validated_data):
         serializer.save()
        else:
            temporary_storage.append(validated_data)
            check_admin_active(self, request, pk)
            print("temporary_storage--->",temporary_storage)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None): # /api/product/<str:id>
        product = Product.objects.get(id=pk)
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })