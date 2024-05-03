# order.urls.py
from django.urls import path
from .views import OrderShopView, OrderProductView, OrderMappingView

urlpatterns = [
    path('shop/<int:shop_id>/', OrderShopView.as_view(), name='shop_orders'),
    path('products/<int:order_shop_id>/', OrderProductView.as_view(), name='order_products'),
    path('mapping/', OrderMappingView.as_view(), name='order_mapping'),
]