# Generated by Django 5.0.6 on 2024-07-26 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0005_remove_orderproduct_color_remove_orderproduct_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(blank=True, max_length=15),
        ),
    ]
