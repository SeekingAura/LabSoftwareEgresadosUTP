# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-05 16:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioEgresado', '0015_auto_20171025_0759'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuarioegresado',
            name='pais',
        ),
        migrations.AlterField(
            model_name='usuarioegresado',
            name='genero',
            field=models.CharField(blank=True, choices=[['masculino', 'Masculino'], ['femenino', 'Femenino'], ['ninguno', 'N/A']], max_length=10),
        ),
    ]
