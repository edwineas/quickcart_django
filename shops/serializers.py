from rest_framework import serializers
from .models import Products, Shops, Inventory
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

class ProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id','name', 'image']

@permission_classes([AllowAny])
class ShopsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = ['shopkeeper', 'name', 'address', 'phone_number', 'opening_time', 'closing_time', 'image']

@permission_classes([AllowAny])
class ShopViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shops
        fields = ['id','name', 'address', 'phone_number', 'opening_time', 'closing_time', 'rating', 'image']

class InventorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = Inventory
        fields = ['id','product_id', 'product_name', 'price', 'quantity']
        read_only_fields = ['id', 'product_id', 'product_name']