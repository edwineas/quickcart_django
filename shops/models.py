from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
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

    def __str__(self):
        return self.name