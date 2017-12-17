
# coding: utf-8

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # 首页
	url(r'^h5', include('h5.urls', namespace='h5')),
	# 管理员后台
	url(r'^admin/', include('web.urls', namespace='web')),
	# 超级后台
	url(r'^superadmin/', admin.site.urls),
]
