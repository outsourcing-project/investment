# coding: utf-8

from django.contrib import admin
from django.contrib.auth.models import User
from web.models import (
    UserInfo,
    Setting,
    Project,
    Attachment,
    Comment,
    ExpertTeam,
    InvestmentTeam,
    InvestmentTeamShow,
    ACL,
)


class UserInfoAdmin(admin.ModelAdmin):

    list_display = ('id', 'user_name', 'openid')


class ACLAdmin(admin.ModelAdmin):
    pass


class SettingAdmin(admin.ModelAdmin):
	pass


class ProjectAdmin(admin.ModelAdmin):
	pass


class AttachmentAdmin(admin.ModelAdmin):
	pass


class CommentAdmin(admin.ModelAdmin):
	pass


class ExpertTeamAdmin(admin.ModelAdmin):
	pass


class InvestmentTeamAdmin(admin.ModelAdmin):
	pass


class InvestmentTeamShowAdmin(admin.ModelAdmin):
	pass


admin.site.register(ACL, ACLAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(Setting, SettingAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(ExpertTeam, ExpertTeamAdmin)
admin.site.register(InvestmentTeam, InvestmentTeamAdmin)
admin.site.register(InvestmentTeamShow, InvestmentTeamShowAdmin)
