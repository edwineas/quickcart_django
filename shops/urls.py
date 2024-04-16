from django.urls import path
from .views import ProductsListView, ShopCreateView, ShopListView, InventoryListView, InventoryUpdateView

urlpatterns = [
    path('products/', ProductsListView.as_view(), name='products-list'),
    path('create/', ShopCreateView.as_view(), name='shop-create'),
    path('list/', ShopListView.as_view(), name='shop-list'),
    path('inventory/<int:shop_id>/', InventoryListView.as_view(), name='inventory-list'),
    path('inventupdate/<int:id>/',InventoryUpdateView.as_view(),name='product-update')
]