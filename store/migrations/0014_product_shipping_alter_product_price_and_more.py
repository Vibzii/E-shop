# Generated by Django 5.0.6 on 2024-08-04 09:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0013_remove_productgallery_variation_variation_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='shipping',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name='variation',
            name='stock',
            field=models.IntegerField(),
        ),
    ]
