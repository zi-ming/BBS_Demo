# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BBS', '0002_article_head_img'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='head_img',
            field=models.ImageField(blank=True, height_field=150, null=True, upload_to='uploads', width_field=150),
        ),
    ]
