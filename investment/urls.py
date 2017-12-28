
# coding: utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from settings import MEDIA_ROOT
from h5.views import index_view


urlpatterns = [
	# 首页
	url(r'^h5', include('h5.urls', namespace='h5')),
	# 管理员后台
	url(r'^admin/', include('web.urls', namespace='web')),
	# 超级后台
	url(r'^superadmin/', admin.site.urls),
	# 上传文件
	url(r"^media/(?P<path>.*)$", serve, {'document_root': MEDIA_ROOT}),
	url(r'^MP_verify_K3P0dE2UJny1YqEW.txt', index_view.validation),
	url(r'^wexin', index_view.wexin, name='wexin'),
]
