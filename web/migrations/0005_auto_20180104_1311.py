# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-01-04 13:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0004_auto_20180102_1350'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='expert_team_email',
            field=models.TextField(blank=True, default='', verbose_name='\u5df2\u53d1\u4e13\u5bb6\u56e2\u90ae\u7bb1'),
        ),
        migrations.AddField(
            model_name='project',
            name='investment_team_email',
            field=models.TextField(blank=True, default='', verbose_name='\u5df2\u53d1\u6295\u8d44\u56e2\u90ae\u7bb1'),
        ),
    ]
