# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-14 17:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('toolsharesite', '0029_auto_20161114_0935'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='transaction',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='toolsharesite.Transaction'),
        ),
        migrations.AlterField(
            model_name='communityshed',
            name='address_line1',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='communityshed',
            name='address_line2',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='communityshed',
            name='city',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='communityshed',
            name='state',
            field=models.CharField(max_length=50),
        ),
    ]
