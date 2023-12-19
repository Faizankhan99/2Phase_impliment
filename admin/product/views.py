from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product, User
from .producer import publish
from .serializers import ProductSerializer
import random 
temporary_storage = []

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
           # Store validated data before calling save
        validated_data = serializer.validated_data
        # validated_data['id'] = pk 
        temporary_storage.append(validated_data)
        print("validated_data -->",validated_data )
        publish('product_updated', validated_data)
        if publish('product_updated', validated_data):
         serializer.save()
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
        publish('product_updated', validated_data)
        if publish('product_updated', validated_data):
         serializer.save()

        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, pk=None): # /api/product/<str:id>
        product = Product.objects.get(id=pk)
        product.delete()
        publish('product_deleted', pk)
        return Response(status=status.HTTP_204_NO_CONTENT)

    

class UserAPIView(APIView):
    def get(self, _):
        users = User.objects.all()
        user = random.choice(users)
        return Response({
            'id': user.id
        })
