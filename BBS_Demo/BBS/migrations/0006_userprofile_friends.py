# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-19 08:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BBS', '0005_auto_20170509_1634'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='friends',
            field=models.ManyToManyField(blank=True, related_name='_userprofile_friends_+', to='BBS.UserProfile'),
        ),
    ]
