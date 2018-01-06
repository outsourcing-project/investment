# coding: utf-8

from django.conf.urls import url

from h5.views import (
    index_view,
    auth_view,
    user_view,
    project_view,
)

# 管理后台
urlpatterns = [
    # 首页
    url(r'^$', index_view.index, name='h5_index'),
    # wechat
    url(r'^wechat/login/$', auth_view.login_wechat, name='login_wechat'),
    url(r'^wechat/callback/$',
        auth_view.login_wechat_callback,
        name='login_wechat_callback'),

    # 用户中心
    url(r'^send_v_code/$', user_view.send_v_code, name='send_v_code'),
    url(r'^user/$', user_view.index, name='user_index'),
    url(r'^user_info/$',
        user_view.person_info, name='person_info'),
    url(r'^user/edit_uname/$',
        user_view.edit_uname, name='edit_uname'),
    url(r'^user/edit_email/$',
        user_view.edit_email, name='edit_email'),
    url(r'^user/edit_mobile/$',
        user_view.edit_mobile, name='edit_mobile'),
    url(r'^user/confirm_mobile/$',
        user_view.confirm_mobile, name='confirm_mobile'),
    url(r'^login/$', user_view.login, name='login'),
    url(r'^login_out/$', user_view.login_out, name='login_out'),
    url(r'^bang_email/$', user_view.bang_email, name='bang_email'),
    url(r'^send_email/$', user_view.send_email, name='send_email'),
    url(r'^user/attachment/$',
        user_view.attachment, name='user_attachment'),
    url(r'^user/project/$',
        user_view.project, name='user_project'),
    url(r'^about/$', user_view.about, name='about'),
    # 项目
    url(r'^project/create/(?P<attachment_id>\d+)/$', project_view.create, name='project_create'),
    url(r'^attachment/(?P<attachment_id>\d+)/$', project_view.attachment, name='project_attachment'),
    url(r'^project/(?P<project_id>\d+)/$', project_view.detail, name='project_detail'),
]
