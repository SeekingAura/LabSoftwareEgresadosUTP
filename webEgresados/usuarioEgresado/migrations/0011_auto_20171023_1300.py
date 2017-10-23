# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 18:00
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioEgresado', '0010_auto_20171021_1747'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='amigosegresado',
            name='userEgre',
        ),
        migrations.RemoveField(
            model_name='interesesegresado',
            name='userEgre',
        ),
        migrations.RenameField(
            model_name='usuariosegresado',
            old_name='userEgre',
            new_name='userAdminEgre',
        ),
        migrations.DeleteModel(
            name='amigosEgresado',
        ),
        migrations.DeleteModel(
            name='interesesEgresado',
        ),
    ]
