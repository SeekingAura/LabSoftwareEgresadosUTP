# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 15:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarioEgresado', '0016_auto_20171112_1643'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuarioegresado',
            name='foto',
            field=models.ImageField(blank=True, default='photo/None/no-img.jpg', null=True, upload_to='photo'),
        ),
    ]