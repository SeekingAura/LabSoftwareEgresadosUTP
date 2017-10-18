# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-17 21:25
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioAdminEgresado', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuariosadminegresado',
            name='DNI',
            field=models.CharField(max_length=30, primary_key=True, serialize=False, validators=[django.core.validators.RegexValidator(message='prueba.', regex='[0-9]*')]),
        ),
    ]