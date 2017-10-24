# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-23 18:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import usuarioEgresado.models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioEgresado', '0011_auto_20171023_1300'),
    ]

    operations = [
        migrations.CreateModel(
            name='AmigosEgresado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amigoDNI', models.CharField(max_length=30)),
                ('estado', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='InteresesEgresado',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interesID', models.CharField(max_length=30, validators=[usuarioEgresado.models.numeric_validator])),
            ],
        ),
        migrations.RenameModel(
            old_name='UsuariosEgresado',
            new_name='UsuarioEgresado',
        ),
        migrations.AddField(
            model_name='interesesegresado',
            name='userEgre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarioEgresado.UsuarioEgresado'),
        ),
        migrations.AddField(
            model_name='amigosegresado',
            name='userEgre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarioEgresado.UsuarioEgresado'),
        ),
    ]