# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-25 12:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioEgresado', '0013_auto_20171023_1338'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuarioegresado',
            name='programa',
            field=models.CharField(choices=[('ingenieria de sistemas', 'ingenieria de sistemas'), ('ingenieria industrial', 'Ingenieria industrial'), ('ingenieria Mecanica', 'Ingenieria Mecanica')], max_length=100),
        ),
    ]
