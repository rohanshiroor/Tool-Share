# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-14 14:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolsharesite', '0028_auto_20161113_1347'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='status',
            field=models.CharField(choices=[('PE', 'Pending'), ('AC', 'Accepted'), ('RJ', 'Rejected'), ('RE', 'Released'), ('CO', 'Complete')], default='PE', max_length=2),
        ),
    ]
