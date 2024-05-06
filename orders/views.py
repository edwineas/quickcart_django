from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderShop, OrderProduct, CacheData
from users.models import Customer
from shops.models import Shops, Inventory, Products
from .serializers import MappingSerializer
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
import googlemaps
import json
import os
from dotenv import load_dotenv


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
        # cache_file = 'cache.json'
        # if os.path.exists(cache_file):
        #     with open(cache_file, 'r') as f:
        #         cache = json.load(f)
        # else:
        #     cache = {}

        selected_shops = []
        remaining_items = cart.copy()
        current_location = user_location
        while remaining_items:
            distances = []
            for shop in shops:
                # Check cache for distance
                cache_key = f'{current_location}_{shop.latitude}_{shop.longitude}'
                cache_data = CacheData.objects.filter(cache_key=cache_key).first()
                if cache_data:
                    distance_value = cache_data.distance_value
                else:
                    # Calculate distance between user and shop
                    distance = gmaps.distance_matrix(current_location, (shop.latitude, shop.longitude))
                    print("requesting distance")
                    # Extract the distance value from the 'distance' object, not 'cache_data'
                    distance_value = distance['rows'][0]['elements'][0]['distance']['value']
                    # Add distance to cache and write to file
                    CacheData.objects.create(cache_key=cache_key, distance_value=distance_value)

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
                            'id': inventory_item.product.id,
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
        serializer = MappingSerializer(selected_shops, many=True)
        print(serializer.data)
        return Response(serializer.data)


class CreateOrderView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            data = request.data

            # Create an Order
            customer = Customer.objects.get(id=data['customer_id'])
            order = Order.objects.create(customer=customer, price=data['total_price'])
            # Create OrderShops and OrderProducts
            for shop_data in data['shops']:
                shop = Shops.objects.get(id=shop_data['shop_id'])
                order_shop = OrderShop.objects.create(order=order, shop=shop, shop_price=shop_data['shop_total_price'], shop_name=shop_data['shop_name'])

                for product_data in shop_data['products']:
                    product = Products.objects.get(id=product_data['product_id'])
                    OrderProduct.objects.create(order_shop=order_shop, product=product, product_name=product_data['product_name'], product_price=product_data['product_price'], product_quantity=product_data['product_quantity'])

            return Response({"message": "Order created successfully","orderid":order.id}, status=status.HTTP_201_CREATED)

        except ObjectDoesNotExist as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([AllowAny])
class PostOrderView(APIView):
    def get(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_shops = OrderShop.objects.filter(order=order)
        response_data = {
            'order_id': order.id,
            'price': order.price,
            'status': order.status,
            'shops': []
        }

        for order_shop in order_shops:
            order_products = OrderProduct.objects.filter(order_shop=order_shop)
            shop_data = {
                'order_shop_id': order_shop.id,
                'shop_id': order_shop.shop.id,
                'shop_name': order_shop.shop_name,
                'shop_price': order_shop.shop_price,
                'packet_picked': order_shop.packet_picked,
                'payment_received': order_shop.payment_received,
                'latitude': order_shop.shop.latitude,
                'longitude': order_shop.shop.longitude,
                'products': []
            }

            for order_product in order_products:
                product_data = {
                    'product': order_product.product.id,
                    'product_name': order_product.product_name,
                    'product_price': order_product.product_price,
                    'product_quantity': order_product.product_quantity
                }
                shop_data['products'].append(product_data)

            response_data['shops'].append(shop_data)

        return Response(response_data)

@permission_classes([AllowAny])
class UpdatePacketPickedView(APIView):
    def post(self, request, order_shop_id):
        order_shop = get_object_or_404(OrderShop, id=order_shop_id)
        order_shop.packet_picked = True
        order_shop.save()

        return Response({"message": "Packet picked status updated successfully"}, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
class CheckPaymentView(APIView):
    def get(self, request, order_shop_id):
        order_shop = get_object_or_404(OrderShop, id=order_shop_id)
        payment_received = order_shop.payment_received

        return Response({"payment_received": payment_received})