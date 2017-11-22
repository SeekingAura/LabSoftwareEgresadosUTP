# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 15:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioAdministrador', '0005_auto_20171112_1739'),
    ]

    operations = [
        migrations.CreateModel(
            name='noticias',
            fields=[
                ('titulo', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('contenido', models.CharField(max_length=500)),
                ('creador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarioAdministrador.UsuarioAdministrador')),
            ],
            options={
                'verbose_name': 'Noticia',
                'verbose_name_plural': 'Noticias',
            },
        ),
        migrations.CreateModel(
            name='noticiasIntereses',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('interes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarioAdministrador.intereses')),
                ('noticia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarioAdministrador.noticias')),
            ],
            options={
                'verbose_name': 'Intereses de noticia',
                'verbose_name_plural': 'Intereses de noticias',
            },
        ),
    ]