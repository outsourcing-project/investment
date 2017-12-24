# coding: utf-8

from django.conf.urls import url

from web.views import (
    index_view,
    account_view,
    acl_view,
    group_view,
    flush_view,
    user_info_view,
    project_view,
    expert_team_view,
    investment_team_view,
    investment_team_show_view,
)

# 管理后台
urlpatterns = [
    url(r'^$', index_view.index, name='index'),

    url(r'^flush/setting/$', flush_view.setting, name='flush_setting'),

    url(r'^login$', account_view.account_login, name='login'),
    url(r'^logout$', account_view.account_logout, name='logout'),

    # 用户管理
    url(r'^user_info$', user_info_view.list, name='user_info_list'),
    url(r'^user_info/(?P<user_info_id>\d+)/freeze$',
        user_info_view.freeze, name='user_info_freeze'),
    url(r'^user_info/(?P<user_info_id>\d+)/thaw$',
        user_info_view.thaw, name='user_info_thaw'),
    url(r'^user_info/(?P<user_info_id>\d+)/delete$',
        user_info_view.delete, name='user_info_delete'),

    # 项目管理
    url(r'^project$', project_view.list, name='project_list'),
    url(r'^project/(?P<project_id>\d+)/top$',
        project_view.top, name='project_top'),
    url(r'^project/(?P<project_id>\d+)/un_top$',
        project_view.un_top, name='project_un_top'),
    url(r'^project/(?P<project_id>\d+)/down_attach$',
        project_view.down_attach, name='project_down_attach'),
    url(r'^project/(?P<project_id>\d+)/delete$',
        project_view.delete, name='project_delete'),

    url(r'^project/comment$',
        project_view.comment_list,
        name='project_comment_list'),
    url(r'^comment/(?P<comment_id>\d+)/delete$',
        project_view.comment_delete, name='project_comment_delete'),

    # 专家团邮箱
    url(r'^expert_team$', expert_team_view.list, name='expert_team_list'),
    url(r'^expert_team/add$', expert_team_view.add, name='expert_team_add'),
    url(r'^expert_team/(?P<expert_team_id>\d+)/edit$',
        expert_team_view.edit, name='expert_team_edit'),
    url(r'^expert_team/(?P<expert_team_id>\d+)/delete$',
        expert_team_view.delete, name='expert_team_delete'),
    url(r'^expert_team/(?P<expert_team_id>\d+)/offline$',
        expert_team_view.offline, name='expert_team_offline'),
    url(r'^expert_team/(?P<expert_team_id>\d+)/online$',
        expert_team_view.online, name='expert_team_online'),

    # 投资团邮箱
    url(r'^investment_team$',
        investment_team_view.list,
        name='investment_team_list'),
    url(r'^investment_team/add$',
        investment_team_view.add,
        name='investment_team_add'),
    url(r'^investment_team/(?P<investment_team_id>\d+)/edit$',
        investment_team_view.edit, name='investment_team_edit'),
    url(r'^investment_team/(?P<investment_team_id>\d+)/delete$',
        investment_team_view.delete, name='investment_team_delete'),
    url(r'^investment_team/(?P<investment_team_id>\d+)/offline$',
        investment_team_view.offline, name='investment_team_offline'),
    url(r'^investment_team/(?P<investment_team_id>\d+)/online$',
        investment_team_view.online, name='investment_team_online'),

    # 投资团展示
    url(r'^investment_team_show$',
        investment_team_show_view.list,
        name='investment_team_show_list'),
    url(r'^investment_team_show/add$',
        investment_team_show_view.add,
        name='investment_team_show_add'),
    url(r'^investment_team_show/(?P<investment_team_show_id>\d+)/edit$',
        investment_team_show_view.edit, name='investment_team_show_edit'),
    url(r'^investment_team_show/(?P<investment_team_show_id>\d+)/delete$',
        investment_team_show_view.delete, name='investment_team_show_delete'),
    url(r'^investment_team_show/(?P<investment_team_show_id>\d+)/up$',
        investment_team_show_view.up, name='investment_team_show_up'),
    url(r'^investment_team_show/(?P<investment_team_show_id>\d+)/down$',
        investment_team_show_view.down, name='investment_team_show_down'),

    url(r'^acl$', acl_view.acl_list, name='acl_list'),
    url(r'^acl/add$', acl_view.acl_add, name='acl_add'),
    url(r'^acl/(?P<acl_id>\d+)/edit$', acl_view.acl_edit, name='acl_edit'),
    url(r'^acl/(?P<acl_id>\d+)/delete$', acl_view.acl_delete, name='acl_delete'),

    url(r'^group$', group_view.group_list, name='group_list'),
    url(r'^group/add$', group_view.group_add, name='group_add'),
    url(r'^group/(?P<group_id>\d+)/edit$',
        group_view.group_edit, name='group_edit'),
    url(r'^group/(?P<group_id>\d+)/delete$',
        group_view.group_delete, name='group_delete'),

    url(r'^account/$', account_view.account_list, name='account_list'),
    url(r'^account/add$', account_view.account_add, name='account_add'),
    url(r'^account/(?P<account_id>\d+)/edit$',
        account_view.account_edit, name='account_edit'),
    url(r'^account/(?P<account_id>\d+)/offline$',
        account_view.account_offline, name='account_offline'),
    url(r'^account/(?P<account_id>\d+)/delete$',
        account_view.account_delete, name='account_delete'),

    url(r'^ckeditor_upload$', index_view.ckeditor_upload, name='admin_upload'),
    url(r'^ckeditor_many_upload$',
        index_view.ckeditor_many_upload,
        name='admin_many_upload'),
]
