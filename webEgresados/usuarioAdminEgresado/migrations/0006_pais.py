# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-19 19:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioAdminEgresado', '0005_auto_20171018_1541'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('paisNombre', models.CharField(max_length=30)),
            ],
        ),
    ]
