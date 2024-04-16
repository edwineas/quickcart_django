# Django management command to populate the Inventory model
from django.core.management.base import BaseCommand
from shops.models import Products, Shops, Inventory

class Command(BaseCommand):
    help = 'Populate the Inventory model with existing products and shops'

    def handle(self, *args, **options):
        for product in Products.objects.all():
            for shop in Shops.objects.all():
                Inventory.objects.get_or_create(product=product, shop=shop, defaults={'price': 0.0, 'quantity': 0})

        self.stdout.write(self.style.SUCCESS('Successfully populated the Inventory model'))