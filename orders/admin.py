from django.contrib import admin
from .models import Order, OrderShop, OrderProduct

# Register your models here.
admin.site.register(Order)
admin.site.register(OrderShop)
admin.site.register(OrderProduct)
