# serializers.py
from rest_framework import serializers
from .models import Order, OrderShop, OrderProduct
from users.models import Customer



class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['id', 'first_name', 'last_name']

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'date', 'customer']

class OrderShopSerializer(serializers.ModelSerializer):
    order = OrderSerializer(read_only=True)

    class Meta:
        model = OrderShop
        fields = ['id','order', 'shop', 'shop_name', 'shop_price', 'packet_picked', 'payment_received']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        order_representation = representation.pop('order')
        representation['order'] = order_representation['id']
        representation['date'] = order_representation['date']
        representation['customer_name'] = f"{order_representation['customer']['first_name']} {order_representation['customer']['last_name']}"
        representation['customer_id'] = order_representation['customer']['id']
        return representation


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product_name', 'product_price', 'product_quantity']