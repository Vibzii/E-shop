# Generated by Django 5.0.6 on 2024-08-08 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0008_alter_order_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='shipping_cost',
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
