# Generated by Django 5.0.4 on 2024-05-01 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0007_remove_shops_latitude_remove_shops_longitude'),
    ]

    operations = [
        migrations.AddField(
            model_name='shops',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='shops',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=20, max_digits=20, null=True),
        ),
    ]
