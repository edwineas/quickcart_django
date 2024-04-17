from django.db import models
from users.models import Customer
from shops.models import Shops, Products

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderShop(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE)
    shop_price = models.DecimalField(max_digits=10, decimal_places=2)

class OrderProduct(models.Model):
    order_shop = models.ForeignKey(OrderShop, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.IntegerField()