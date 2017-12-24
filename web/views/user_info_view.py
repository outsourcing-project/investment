# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from web.models import (
    UserInfo,
)

from utils.paging_utils import (
    paging_objs,
)
from utils.qiniu_utils import (
    get_extension,
    handle_uploaded_file,
)

import time


@staff_member_required(login_url='/admin/login')
def list(request):

    context = {}
    context['module'] = 'user'
    objs = UserInfo.obs.get_queryset().order_by('-created')

    search_name = request.GET.get('search_name', None)
    if search_name:
        context['search_name'] = search_name
        objs = objs.filter(Q(nickname__icontains=search_name) | Q(user_name__icontains=search_name))

    page = request.GET.get('page', 1)
    user_infos = paging_objs(object_list=objs, per_page=10, page=page)

    context['page'] = page
    context['clients'] = user_infos

    return render(request, 'web/userinfo/index.html', context)


@staff_member_required(login_url='/admin/login')
def delete(request, user_info_id):
    page = request.GET.get('page', 1)
    search_name = request.GET.get('search_name', '')
    user_info = UserInfo.objects.get(id=user_info_id)
    user_info.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

@staff_member_required(login_url='/admin/login')
def freeze(request, user_info_id):
    page = request.GET.get('page', 1)
    search_name = request.GET.get('search_name', '')
    user_info = UserInfo.objects.get(id=user_info_id)
    user_info.deactivate()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def thaw(request, user_info_id):
    page = request.GET.get('page', 1)
    search_name = request.GET.get('search_name', '')
    user_info = UserInfo.objects.get(id=user_info_id)
    user_info.activate()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
