from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, serializers
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Customer, Shopkeeper
from shops.models import Shops
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate



# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        try:
            if Customer.objects.filter(user=user).exists():
                customer = Customer.objects.get(user=user)
                token['role'] = 'customer'
                token['customer_id'] = customer.id
            elif Shopkeeper.objects.filter(user=user).exists():
                shopkeeper = Shopkeeper.objects.get(user=user)
                shop = Shops.objects.get(shopkeeper=shopkeeper)
                token['role'] = 'shopkeeper'
                token['shop_id'] = shop.id     
                token['shopkeeper_id'] = shopkeeper.id 
            else:
                token['role'] = 'unknown'
        except (Customer.DoesNotExist, Shopkeeper.DoesNotExist) as e:
            token['role'] = 'unknown'
            
        return token
    
    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')

        if username and not User.objects.filter(username=username).exists():
            raise serializers.ValidationError('User does not exist.', code='user_not_found')

        user = authenticate(username=username, password=password)

        if not user:
            raise serializers.ValidationError('Incorrect password.', code='incorrect_password')

        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['role'] = refresh['role']
        data['user_id'] = self.user.id
        if refresh['role'] == 'shopkeeper':
            data['shop_id'] = refresh['shop_id']
            data['shopkeeper_id'] = refresh['shopkeeper_id']
        elif refresh['role'] == 'customer':
            data['customer_id'] = refresh['customer_id']

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer