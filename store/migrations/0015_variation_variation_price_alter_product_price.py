# Generated by Django 5.0.6 on 2024-08-04 09:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_product_shipping_alter_product_price_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variation',
            name='variation_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]