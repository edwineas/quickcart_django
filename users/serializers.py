from rest_framework import serializers
from .models import Customer, Shopkeeper

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'first_name', 'last_name', 'email', 'phone_number']

class ShopkeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopkeeper
        fields = ['user', 'first_name', 'last_name', 'email', 'phone_number']