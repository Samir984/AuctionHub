# Generated by Django 5.1.2 on 2024-10-25 08:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0002_remove_bid_bid_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auction',
            name='item',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='marketplace.item'),
        ),
    ]