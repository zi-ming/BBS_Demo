# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-09 08:33
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BBS', '0003_auto_20170509_1632'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='head_img',
            field=models.ImageField(upload_to='uploads'),
        ),
    ]
