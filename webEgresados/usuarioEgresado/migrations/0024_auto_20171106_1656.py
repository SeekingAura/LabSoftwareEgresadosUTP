# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-06 21:56
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioEgresado', '0023_auto_20171106_1639'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarioegresado',
            name='promoteAge',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
