from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from users.models import Customer, Shopkeeper
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


# Create your views here.
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        try:
            if Customer.objects.filter(user=user).exists():
                token['role'] = 'customer'
            elif Shopkeeper.objects.filter(user=user).exists():
                token['role'] = 'shopkeeper'
            else:
                token['role'] = 'unknown'
        except (Customer.DoesNotExist, Shopkeeper.DoesNotExist) as e:
            token['role'] = 'unknown'
            
        return token
    
    def validate(self, attrs):
        data = super().validate(attrs)

        refresh = self.get_token(self.user)
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        # Add extra responses here
        data['role'] = refresh['role']
        data['user_id'] = self.user.id

        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer