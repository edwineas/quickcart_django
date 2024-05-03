# views.py
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import OrderShop, OrderProduct
from shops.models import Shops, Inventory
from .serializers import OrderShopSerializer, OrderProductSerializer, OrderSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
import googlemaps
import json
import os
from dotenv import load_dotenv




@permission_classes([AllowAny])
class OrderShopView(APIView):
    def get(self, request, shop_id):
        ordershop = OrderShop.objects.filter(shop__id__exact=shop_id)
        serializer = OrderShopSerializer(ordershop, many=True)
        return Response(serializer.data)

@permission_classes([AllowAny])
class OrderProductView(APIView):
    def get(self, request, order_shop_id):
        order_products = OrderProduct.objects.filter(order_shop_id=order_shop_id)
        serializer = OrderProductSerializer(order_products, many=True)
        return Response(serializer.data)
    
@permission_classes([AllowAny])
class OrderMappingView(APIView):
    def post(self, request):
        print("request check-in")
        print(request.data)

        # Get cart data and user location from request data
        cart = request.data.get('cartItems')
        user_location = request.data.get('location')
        load_dotenv()  # take environment variables from .env.
        gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
        shops = Shops.objects.all()
        cache_file = 'cache.json'
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
        else:
            cache = {}

        selected_shops = []
        remaining_items = cart.copy()
        current_location = user_location
        while remaining_items:
            distances = []
            for shop in shops:
                # Check cache for distance
                cache_key = f'{current_location}_{shop.latitude}_{shop.longitude}'
                if cache_key in cache:
                    distance_value = cache[cache_key]
                else:
                    # Calculate distance between user and shop
                    distance = gmaps.distance_matrix(current_location, (shop.latitude, shop.longitude))
                    print("requesting distance")

                    # Extract the distance value
                    distance_value = distance['rows'][0]['elements'][0]['distance']['value']

                    # Add distance to cache and write to file
                    cache[cache_key] = distance_value
                    with open(cache_file, 'w') as f:
                        json.dump(cache, f)

                distances.append((shop, distance_value))

            # Sort shops by distance
            distances.sort(key=lambda x: x[1])

            # Select nearest shop with required product
            for shop, distance in distances:
                shop_info = {
                    'shop': shop,
                    'shop_name': shop.name,
                    'shop_rating': shop.rating,
                    'products': [],
                    'total_price': 0
                }
                for item in remaining_items.copy():
                    inventory = Inventory.objects.filter(shop=shop, product__name=item['name'])
                    if inventory.exists() and inventory.first().quantity >= item['quantity']:
                        inventory_item = inventory.first()
                        product_price = inventory_item.price * item['quantity']
                        shop_info['products'].append({
                            'product': inventory_item.product, 
                            'quantity': item['quantity'], 
                            'price': product_price
                        })
                        shop_info['total_price'] += product_price
                        remaining_items.remove(item)
                if shop_info['products']:
                    selected_shops.append(shop_info)
                    current_location = (shop.latitude, shop.longitude)
                    break
        # Serialize and return response
        serializer = OrderSerializer(selected_shops, many=True)
        print(serializer.data)
        return Response(serializer.data)