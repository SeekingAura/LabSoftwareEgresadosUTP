# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 17:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioEgresado', '0016_auto_20171105_1158'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioegresado',
            name='fechaGraduado',
            field=models.DateField(blank=True, null=True),
        ),
    ]
