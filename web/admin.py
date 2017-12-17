# coding: utf-8

from django.contrib import admin
from django.contrib.auth.models import User
from web.models import (
    UserInfo,
    Setting,
)

class UserInfoAdmin(admin.ModelAdmin):

    list_display = ('id', 'user_name', 'openid')

class SettingAdmin(admin.ModelAdmin):
	pass


admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Setting, SettingAdmin)

