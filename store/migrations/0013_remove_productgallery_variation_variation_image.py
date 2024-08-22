# Generated by Django 5.0.6 on 2024-08-03 19:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_alter_productgallery_variation'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productgallery',
            name='variation',
        ),
        migrations.AddField(
            model_name='variation',
            name='image',
            field=models.ImageField(default=None, max_length=255, upload_to='store/products/'),
            preserve_default=False,
        ),
    ]