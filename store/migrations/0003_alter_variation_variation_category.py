# Generated by Django 5.0.6 on 2024-07-01 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='variation_category',
            field=models.CharField(choices=[('color', 'color'), ('size', 'size'), ('sets', 'sets')], max_length=100),
        ),
    ]
