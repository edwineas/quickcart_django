# Generated by Django 5.0.4 on 2024-05-01 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shops', '0004_inventory'),
    ]

    operations = [
        migrations.AddField(
            model_name='shops',
            name='latitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
        migrations.AddField(
            model_name='shops',
            name='longitude',
            field=models.DecimalField(blank=True, decimal_places=6, max_digits=9, null=True),
        ),
    ]