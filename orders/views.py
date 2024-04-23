# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OrderShop
from .serializers import OrderSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes

@permission_classes([AllowAny])
class OrderShopView(APIView):
    def get(self, request, shop_id):
        ordershop = OrderShop.objects.filter(shop_id=shop_id)
        serializer = OrderSerializer(ordershop, many=True)
        return Response(serializer.data)