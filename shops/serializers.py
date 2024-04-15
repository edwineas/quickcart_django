from rest_framework import serializers
from .models import Products, Shops
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['name', 'image']

@permission_classes([AllowAny])
class ShopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = ['shopkeeper', 'name', 'address', 'phone_number', 'opening_time', 'closing_time', 'image']

@permission_classes([AllowAny])
class ShopViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = ['name', 'address', 'phone_number', 'opening_time', 'closing_time', 'rating', 'image']