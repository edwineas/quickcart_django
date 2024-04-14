from rest_framework import serializers
from .models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = ['user', 'first_name', 'last_name', 'email', 'phone_number']