# serializers.py
from rest_framework import serializers
from .models import Order, OrderShop, OrderProduct
from users.models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id','user', 'first_name', 'last_name', 'email', 'phone_number']
        
class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['order_shop', 'product','product_name', 'product_price', 'product_quantity']

class OrderShopSerializer(serializers.ModelSerializer):
    products = OrderProductSerializer(many=True, read_only=True)
    class Meta:
        model = OrderShop
        fields = ['order', 'shop','shop_name', 'shop_price', 'packet_picked', 'payment_received', 'products']

class OrderSerializer(serializers.ModelSerializer):
    shops = OrderShopSerializer(many=True, read_only=True)
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'date', 'customer', 'price', 'status', 'shops']