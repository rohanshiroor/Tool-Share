# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-09 21:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toolsharesite', '0007_auto_20161009_1326'),
    ]

    operations = [
        migrations.RenameField(
            model_name='communityshed',
            old_name='address_line_1',
            new_name='address_line1',
        ),
        migrations.RenameField(
            model_name='communityshed',
            old_name='address_line_2',
            new_name='address_line2',
        ),
    ]
