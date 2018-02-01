# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-10 00:58
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('toolsharesite', '0011_auto_20161009_2051'),
    ]

    operations = [
        migrations.RenameField(
            model_name='communityshed',
            old_name='share_zone_id',
            new_name='share_zone',
        ),
        migrations.RenameField(
            model_name='feedback',
            old_name='tool_id',
            new_name='tool',
        ),
        migrations.RenameField(
            model_name='notification',
            old_name='transaction_id',
            new_name='transaction',
        ),
        migrations.RenameField(
            model_name='toolshareuser',
            old_name='role_id',
            new_name='role',
        ),
        migrations.RenameField(
            model_name='toolshareuser',
            old_name='share_zone_id',
            new_name='share_zone',
        ),
        migrations.RenameField(
            model_name='transaction',
            old_name='tool_id',
            new_name='tool',
        ),
        migrations.RemoveField(
            model_name='tool',
            name='community_shed_id',
        ),
        migrations.AddField(
            model_name='tool',
            name='community_shed',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='toolsharesite.CommunityShed'),
        ),
    ]