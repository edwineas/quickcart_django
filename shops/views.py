from rest_framework import generics
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from .models import Products, Shops
from .serializers import ProductsSerializer, ShopsSerializer

@permission_classes([AllowAny])
class ProductsListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    
@permission_classes([AllowAny])
class ShopCreateView(generics.CreateAPIView):
    queryset = Shops.objects.all()
    serializer_class = ShopsSerializer