# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-02 00:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioAdminEgresado', '0012_auto_20171101_1920'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuariosadminegresado',
            name='departamento',
        ),
        migrations.AddField(
            model_name='usuariosadminegresado',
            name='departamento',
            field=models.CharField(blank=True, max_length=30),
        ),
    ]
