# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-11-10 18:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('toolsharesite', '0024_auto_20161110_1320'),
    ]

    operations = [
        migrations.RenameField(
            model_name='tool',
            old_name='pickUpPref',
            new_name='pick_up_preference',
        ),
        migrations.RenameField(
            model_name='tool',
            old_name='specialInstruction',
            new_name='special_instruction',
        ),
    ]
