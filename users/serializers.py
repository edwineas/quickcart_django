from rest_framework import serializers
from .models import Customer, Shopkeeper
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@permission_classes([AllowAny])
class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'first_name', 'last_name', 'email', 'phone_number']

@permission_classes([AllowAny])
class ShopkeeperSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shopkeeper
        fields = ['user', 'first_name', 'last_name', 'email', 'phone_number']