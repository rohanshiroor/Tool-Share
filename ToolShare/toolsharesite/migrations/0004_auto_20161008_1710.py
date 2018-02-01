# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-08 21:10
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
        ('toolsharesite', '0003_auto_20161008_1434'),
    ]

    operations = [
        migrations.CreateModel(
            name='ToolShareUser',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address_line1', models.CharField(max_length=100)),
                ('address_line2', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('zip', models.BigIntegerField()),
                ('phone_no', models.BigIntegerField()),
                ('created_date', models.DateField()),
                ('updated_date', models.DateField()),
                ('share_zone_id', models.BigIntegerField()),
                ('role_id', models.BigIntegerField()),
            ],
            options={
                'verbose_name_plural': 'users',
                'verbose_name': 'user',
                'abstract': False,
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.DeleteModel(
            name='User',
        ),
    ]