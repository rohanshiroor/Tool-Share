# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-06 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolsharesite', '0022_auto_20161105_1913'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='image',
            field=models.ImageField(upload_to='uploads/'),
        ),
    ]