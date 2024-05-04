# serializers.py
from rest_framework import serializers
from .models import Order, OrderShop, OrderProduct
from shops.serializers import ShopsSerializer
from users.models import Customer



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name']

class ProductSerializer(serializers.Serializer):
    product = serializers.StringRelatedField()
    quantity = serializers.IntegerField()
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

class MappingSerializer(serializers.Serializer):
    shop = ShopsSerializer()
    shop_name = serializers.CharField()
    shop_rating = serializers.FloatField()
    products = ProductSerializer(many=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2)