# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-13 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UsuariosEgresado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=25)),
                ('apellidos', models.CharField(max_length=50)),
                ('departamento', models.CharField(max_length=30)),
                ('ciudad', models.CharField(max_length=30)),
                ('direccion', models.CharField(max_length=100)),
                ('telefono', models.CharField(max_length=15)),
                ('estadoCuenta', models.CharField(max_length=15)),
            ],
        ),
    ]