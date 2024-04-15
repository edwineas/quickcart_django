from django.urls import path
from .views import ProductsListView, ShopCreateView

urlpatterns = [
    path('products/', ProductsListView.as_view(), name='products-list'),
    path('create/', ShopCreateView.as_view(), name='shop-create'),
]