from django.db import models
from users.models import Customer
from shops.models import Shops, Products

class Order(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=255, default='Pending')
    
    def __str__(self):
        return f"{self.customer.user.username} {self.id}"

class OrderShop(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE)
    shop_price = models.DecimalField(max_digits=10, decimal_places=2)
    shop_name = models.CharField(max_length=255, null=True, blank=True)
    packet_picked = models.BooleanField(default=False)
    payment_received = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.order.customer.user.username} {self.shop.name} {self.id}"

class OrderProduct(models.Model):
    order_shop = models.ForeignKey(OrderShop, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    product_name = models.CharField(max_length=255, null=True, blank=True) 
    product_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_quantity = models.IntegerField()
    
    def __str__(self):
        return f"{self.order_shop.order.customer.user.username} {self.product.name} in {self.order_shop.shop.name}"

class CacheData(models.Model):
    cache_key = models.CharField(max_length=255, unique=True)
    distance_value = models.FloatField()