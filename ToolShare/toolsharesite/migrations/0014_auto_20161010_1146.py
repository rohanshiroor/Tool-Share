# -*- coding: utf-8 -*-
# Generated by Django 1.9.1 on 2016-10-10 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolsharesite', '0013_auto_20161009_2100'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tool',
            name='category',
            field=models.CharField(choices=[('OT', 'Other'), ('CV', 'Clamps & Vises'), ('AC', 'Air Compressors'), ('FT', 'Fastener Tools'), ('HT', 'Hand Tools'), ('KS', 'Knives, Blades & Sharpeners'), ('LT', 'Layout & Measuring Tools'), ('FL', 'Flashlights & Portable Lighting'), ('PT', 'Power Tools'), ('PE', 'Protective & Safety Equipment'), ('TS', 'Tool Holders & Storage'), ('WV', 'Wet/Dry Vacuums'), ('WS', 'Work Benches & Sawhorses'), ('TS', 'Tile Saws')], default='OT', max_length=2),
        ),
        migrations.AlterField(
            model_name='tool',
            name='status',
            field=models.CharField(choices=[('AV', 'Available'), ('BO', 'Borrowed'), ('DA', 'Deactivated'), ('RE', 'Reserved')], default='AV', max_length=100),
        ),
    ]
