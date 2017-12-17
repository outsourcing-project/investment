# coding: utf-8

from django.conf.urls import url

from web.views import (
    index_view,
    account_view,
    acl_view,
    group_view,
    flush_view,
)

# 管理后台
urlpatterns = [
    url(r'^$', index_view.index, name='index'),

    url(r'^flush/setting/$', flush_view.setting, name='flush_setting'),

    url(r'^login$', account_view.account_login, name='login'),
    url(r'^logout$', account_view.account_logout, name='logout'),

    url(r'^acl$', acl_view.acl_list, name='acl_list'),
    url(r'^acl/add$', acl_view.acl_add, name='acl_add'),
    url(r'^acl/(?P<acl_id>\d+)/edit$', acl_view.acl_edit, name='acl_edit'),
    url(r'^acl/(?P<acl_id>\d+)/delete$', acl_view.acl_delete, name='acl_delete'),

    url(r'^group$', group_view.group_list, name='group_list'),
    url(r'^group/add$', group_view.group_add, name='group_add'),
    url(r'^group/(?P<group_id>\d+)/edit$', group_view.group_edit, name='group_edit'),
    url(r'^group/(?P<group_id>\d+)/delete$', group_view.group_delete, name='group_delete'),

    url(r'^account/$', account_view.account_list, name='account_list'),
    url(r'^account/add$', account_view.account_add, name='account_add'),
    url(r'^account/(?P<account_id>\d+)/edit$', account_view.account_edit, name='account_edit'),
    url(r'^account/(?P<account_id>\d+)/offline$', account_view.account_offline, name='account_offline'),
    url(r'^account/(?P<account_id>\d+)/delete$', account_view.account_delete, name='account_delete'),

    url(r'^ckeditor_upload$', index_view.ckeditor_upload, name='admin_upload'),
    url(r'^ckeditor_many_upload$', index_view.ckeditor_many_upload, name='admin_many_upload'),
]
