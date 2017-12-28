# coding: utf-8

from django.conf.urls import url

from h5.views import (
    index_view,
    auth_view,
)

# 管理后台
urlpatterns = [
    # 首页
    url(r'^$', index_view.index, name='h5_index'),
    # wechat
    url(r'^wechat/login/$', auth_view.login_wechat, name='login_wechat'),
    url(r'^wechat/callback/$', auth_view.login_wechat_callback, name='login_wechat_callback'),
    # 个人中心


]
