from django.urls import path
from .views import CustomerRegisterView, ShopkeeperRegisterView

urlpatterns = [
    path('customer/', CustomerRegisterView.as_view(), name='customer_register'),
    path('shopkeeper/', ShopkeeperRegisterView.as_view(), name='shopkeeper_register')
]