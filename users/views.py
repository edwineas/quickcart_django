from rest_framework.response import Response
from rest_framework import status, generics
from .models import Customer
from .serializers import CustomerSerializer
from django.contrib.auth.models import User
from api.serializers import UserSerializer
from rest_framework.permissions import AllowAny


class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        user_data = {
            'username': request.data.get('username'),
            'password': request.data.get('password')
        }
        user_serializer = UserSerializer(data=user_data)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()  # Create the user instance using the serializer's create method

        customer_data = {
            'user': user.id,
            'first_name': request.data.get('first_name'),
            'last_name': request.data.get('last_name'),
            'email': request.data.get('email'),
            'phone_number': request.data.get('phone_number')
        }
        customer_serializer = CustomerSerializer(data=customer_data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            return Response({'status': 'success', 'data': customer_serializer.data}, status=status.HTTP_201_CREATED)
        else:
            user.delete()  # Delete the user instance if customer data is invalid
            return Response({'status': 'error', 'message': 'Invalid customer data', 'errors': customer_serializer.errors}, status=status.HTTP_400_BAD_REQUEST)