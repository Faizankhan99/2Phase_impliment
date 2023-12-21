from django.urls import path
from .views import ProductViewSet,UserAPIView

urlpatterns = [
  
    path('test', ProductViewSet.as_view({
        'get':'list',
    })),

    path('product', ProductViewSet.as_view({
        'get':'list',
        'post':'create'
    })),
    path('product/<str:pk>', ProductViewSet.as_view({
        'get':'retrieve',
        'put':'update',
        'delete':'destroy'
    })),
    path('user',UserAPIView.as_view())
]
