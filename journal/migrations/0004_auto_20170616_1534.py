# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 06:34
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('journal', '0003_auto_20170616_1518'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Posts',
            new_name='Post',
        ),
    ]
