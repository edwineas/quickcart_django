from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save
from django.dispatch import receiver
from users.models import Shopkeeper

# model for Products
class Products(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')
    
    def __str__(self):
        return self.name

# model for Shops
class Shops(models.Model):
    shopkeeper = models.ForeignKey(Shopkeeper, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    opening_time = models.TimeField()
    closing_time = models.TimeField()
    rating = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(5.0)],null=True, blank=True)
    image = models.ImageField(upload_to='shops/')
    latitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)
    longitude = models.DecimalField(max_digits=20, decimal_places=15, null=True, blank=True)


    def __str__(self):
        return str(self.id)

# model for Inventory   
class Inventory(models.Model):
    shop = models.ForeignKey(Shops, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0.0)])
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} in {self.shop.name}"
    
@receiver(post_save, sender=Products)
def create_inventory_for_new_product(sender, instance, created, **kwargs):
    if created:
        for shop in Shops.objects.all():
            Inventory.objects.get_or_create(product=instance, shop=shop, defaults={'price': 0.0, 'quantity': 0})

@receiver(post_save, sender=Shops)
def create_inventory_for_new_shop(sender, instance, created, **kwargs):
    if created:
        for product in Products.objects.all():
            Inventory.objects.get_or_create(shop=instance, product=product, defaults={'price': 0.0, 'quantity': 0})