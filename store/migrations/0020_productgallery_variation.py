# Generated by Django 5.0.6 on 2024-08-14 11:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0019_alter_product_price_alter_product_shipping_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='productgallery',
            name='variation',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
    ]
