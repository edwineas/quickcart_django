from rest_framework import generics, status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from .models import Products, Shops, Inventory
from .serializers import ProductsSerializer, ShopsSerializer, ShopViewSerializer, InventorySerializer
from rest_framework.exceptions import NotFound


@permission_classes([AllowAny])
class ProductsListView(generics.ListAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductsSerializer
    
    
@permission_classes([AllowAny])
class ShopCreateView(generics.CreateAPIView):
    queryset = Shops.objects.all()
    serializer_class = ShopsSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({"status": "success", "data": serializer.data}, status=status.HTTP_201_CREATED, headers=headers)
        return Response({"status": "error", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@permission_classes([AllowAny])
class ShopListView(generics.ListAPIView):
    queryset = Shops.objects.all()
    serializer_class = ShopViewSerializer

@permission_classes([AllowAny])
class InventoryListView(generics.ListAPIView):
    serializer_class = InventorySerializer

    def get_queryset(self):
        shop_id = self.kwargs['shop_id']
        inventory_items = Inventory.objects.filter(shop_id=shop_id)
        if not inventory_items:
            raise NotFound('Shop not found')
        return inventory_items

@permission_classes([AllowAny])
class InventoryUpdateView(generics.UpdateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    lookup_field = 'id'
