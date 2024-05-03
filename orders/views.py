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

        # Initialize Google Maps client
        load_dotenv()  # take environment variables from .env.
        gmaps = googlemaps.Client(key=os.getenv('GOOGLE_MAPS_API_KEY'))
        # Retrieve shop data
        shops = Shops.objects.all()

        # Load cache file
        cache_file = 'cache.json'
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as f:
                cache = json.load(f)
        else:
            cache = {}

        # Calculate distances and select shops
        selected_shops = []
        for item in cart:
            distances = []
            for shop in shops:
                # Determine the start location for distance calculation
                if not selected_shops:
                    start_location = user_location
                else:
                    start_location = (selected_shops[-1].latitude, selected_shops[-1].longitude)

                # Check cache for distance
                cache_key = f'{start_location}_{shop.latitude}_{shop.longitude}'
                if cache_key in cache:
                    distance_value = cache[cache_key]
                else:
                    # Calculate distance between start location and shop
                    distance = gmaps.distance_matrix(start_location, (shop.latitude, shop.longitude))
                    distance_value = distance['rows'][0]['elements'][0]['distance']['value']
                    # Cache the calculated distance
                    cache[cache_key] = distance_value

                distances.append((distance_value, shop))

            # Select the shop with the shortest distance
            distances.sort(key=lambda x: x[0])
            selected_shop = distances[0][1]
            selected_shops.append(selected_shop)

        # Save cache to file
        with open(cache_file, 'w') as f:
            json.dump(cache, f)

            # Select nearest shop with required product
            for shop, distance in distances:
                inventory = Inventory.objects.filter(shop=shop, product__name=item['name'])
                if inventory.exists() and inventory.first().quantity >= item['quantity']:
                    inventory_item = inventory.first()
                    product_price = inventory_item.price * item['quantity']
                    
                    # Check if shop is already in selected_shops
                    shop_info = next((s for s in selected_shops if s['shop'] == shop), None)
                    if shop_info:
                        # If shop is already in selected_shops, add product to its list and update total price
                        shop_info['products'].append({
                            'product': inventory_item.product, 
                            'quantity': item['quantity'], 
                            'price': product_price
                        })
                        shop_info['total_price'] += product_price
                    else:
                        # If shop is not in selected_shops, add it with the product and initial total price
                        selected_shops.append({
                            'shop': shop,
                            'shop_name': shop.name,
                            'shop_rating': shop.rating,
                            'products': [{
                                'product': inventory_item.product, 
                                'quantity': item['quantity'], 
                                'price': product_price
                            }],
                            'total_price': product_price
                        })
                    break

        # Serialize and return response
        serializer = OrderSerializer(selected_shops, many=True)
        print(serializer.data)
        return Response(serializer.data)