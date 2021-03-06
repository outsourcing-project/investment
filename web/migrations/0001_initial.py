# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-12-17 15:51
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ACL',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_del', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5220\u9664')),
                ('is_valid', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('module', models.CharField(default='', max_length=255, verbose_name='\u6a21\u5757\u540d\u79f0')),
                ('module_cn', models.CharField(default='', max_length=255, verbose_name='\u6a21\u5757\u4e2d\u6587\u540d\u79f0')),
                ('permission_ids', models.CharField(default='', max_length=255, verbose_name='\u6743\u9650\u9009\u9879')),
            ],
            options={
                'verbose_name': '\u8bbf\u95ee\u63a7\u5236\u5217\u8868',
                'verbose_name_plural': '\u8bbf\u95ee\u63a7\u5236\u5217\u8868',
                'permissions': (('view_module', '\u67e5\u770b'), ('add_module', '\u6dfb\u52a0'), ('edit_module', '\u7f16\u8f91'), ('delete_module', '\u5220\u9664'), ('active_module', '\u542f\u7528\u7981\u7528'), ('move_module', '\u4e0a\u79fb\u4e0b\u79fb')),
            },
        ),
        migrations.CreateModel(
            name='Setting',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_del', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5220\u9664')),
                ('is_valid', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('name', models.CharField(default='', max_length=100, verbose_name='\u5b57\u6bb5')),
                ('value', models.CharField(default='', max_length=100, verbose_name='\u503c')),
                ('code', models.CharField(default='', max_length=100, verbose_name='code')),
            ],
            options={
                'verbose_name': '\u914d\u7f6e',
                'verbose_name_plural': '\u914d\u7f6e',
            },
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_del', models.BooleanField(default=False, verbose_name='\u662f\u5426\u5220\u9664')),
                ('is_valid', models.BooleanField(default=True, verbose_name='\u662f\u5426\u53ef\u7528')),
                ('updated', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('created', models.DateTimeField(auto_now_add=True, null=True, verbose_name='\u521b\u5efa\u65f6\u95f4')),
                ('email', models.CharField(blank=True, default='', max_length=128, verbose_name='\u90ae\u7bb1')),
                ('user_name', models.CharField(default='', max_length=128, verbose_name='\u59d3\u540d')),
                ('nickname', models.CharField(default='', max_length=128, verbose_name='\u6635\u79f0')),
                ('password', models.CharField(blank=True, default='', max_length=255, verbose_name='\u5bc6\u7801')),
                ('jwt_token', models.TextField(blank=True, default='', null=True, verbose_name='jwt_token')),
                ('openid', models.CharField(default='', max_length=255, verbose_name='openid')),
                ('user_login_type', models.IntegerField(choices=[(1, '\u624b\u673a\u7528\u6237'), (2, '\u5fae\u4fe1\u7528\u6237'), (3, '\u5fae\u535a\u7528\u6237'), (4, 'qq')], default=1, verbose_name='\u7528\u6237\u6ce8\u518c\u7c7b\u578b')),
                ('gender', models.IntegerField(choices=[(1, '\u7537'), (2, '\u5973')], default=1, verbose_name='\u6027\u522b')),
                ('age', models.IntegerField(default=0, verbose_name='\u5e74\u9f84')),
                ('mobile', models.CharField(blank=True, default='', max_length=16, verbose_name='\u624b\u673a')),
                ('avatar', models.CharField(blank=True, default='', max_length=300, null=True, verbose_name='\u5934\u50cf')),
                ('birbath', models.DateField(default=datetime.date.today, verbose_name='\u751f\u65e5')),
                ('wx_unionid', models.CharField(blank=True, default='', max_length=300, verbose_name='\u5fae\u4fe1id')),
                ('weibo_uid', models.CharField(blank=True, default='', max_length=300, verbose_name='\u5fae\u535aid')),
                ('qq_uid', models.CharField(blank=True, default='', max_length=300, verbose_name='qqid')),
                ('user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='\u7528\u6237')),
            ],
            options={
                'verbose_name': '\u7528\u6237\u4fe1\u606f',
                'verbose_name_plural': '\u7528\u6237\u4fe1\u606f',
            },
        ),
    ]
