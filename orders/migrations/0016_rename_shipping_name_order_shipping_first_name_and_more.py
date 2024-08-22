# Generated by Django 5.0.6 on 2024-08-12 11:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0015_alter_orderproduct_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='shipping_name',
            new_name='shipping_first_name',
        ),
        migrations.AddField(
            model_name='order',
            name='house_number',
            field=models.CharField(default=0, max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_house_number',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='order',
            name='shipping_last_name',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]