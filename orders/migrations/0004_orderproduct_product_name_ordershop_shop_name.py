# Generated by Django 5.0.4 on 2024-04-18 14:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0003_order_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderproduct',
            name='product_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='ordershop',
            name='shop_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
