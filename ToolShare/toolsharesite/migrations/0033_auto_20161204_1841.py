# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-12-04 23:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolsharesite', '0032_auto_20161202_2213'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='image',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
