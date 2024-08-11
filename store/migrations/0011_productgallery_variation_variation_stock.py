# Generated by Django 5.0.6 on 2024-08-03 12:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0010_remove_variation_stock'),
    ]

    operations = [
        migrations.AddField(
            model_name='productgallery',
            name='variation',
            field=models.ForeignKey(blank=True, default=None, on_delete=django.db.models.deletion.CASCADE, to='store.variation'),
        ),
        migrations.AddField(
            model_name='variation',
            name='stock',
            field=models.IntegerField(default=0),
        ),
    ]
