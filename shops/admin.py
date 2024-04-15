from django.contrib import admin
from .models import Products, Shops, Inventory

# Register your models here.
admin.site.register(Products)
admin.site.register(Shops)
admin.site.register(Inventory)