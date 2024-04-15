from django.db import models

# model for Products
class Products(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/')