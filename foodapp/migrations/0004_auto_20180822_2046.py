# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-22 15:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0003_order_delivered'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantprofileinfo',
            name='restaurant_noofmenu',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='restaurantprofileinfo',
            name='restaurant_nooforder',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='restaurantprofileinfo',
            name='restaurant_noofrating',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='restaurantprofileinfo',
            name='restaurant_totalrating',
            field=models.IntegerField(default=0),
        ),
    ]