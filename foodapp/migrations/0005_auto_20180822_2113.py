# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-08-22 15:43
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('foodapp', '0004_auto_20180822_2046'),
    ]

    operations = [
        migrations.RenameField(
            model_name='restaurantprofileinfo',
            old_name='restaurant_totalrating',
            new_name='restaurant_avgrating',
        ),
    ]