from django.db import models
from django.contrib.auth.models import User

# mode for Customer
class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name

# model for Shopkeeper
class Shopkeeper(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return self.first_name + ' ' + self.last_name