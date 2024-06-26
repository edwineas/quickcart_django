from django.urls import path
from .views import CustomerRegisterView, ShopkeeperRegisterView, UserNameView, CustomerView

urlpatterns = [
    path('customer/', CustomerRegisterView.as_view(), name='customer_register'),
    path('shopkeeper/', ShopkeeperRegisterView.as_view(), name='shopkeeper_register'),
    path('name/<int:user_id>/', UserNameView.as_view(), name='user_name'),
    path('customer/<int:customer_id>/', CustomerView.as_view(), name='customer'),
]