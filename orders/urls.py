# order.urls.py
from django.urls import path
from .views import OrderShopView

urlpatterns = [
    path('shop/<int:shop_id>/', OrderShopView.as_view(), name='shop_orders'),
]