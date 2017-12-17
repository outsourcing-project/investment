# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models import Max, Min
from web.models import (
    UserInfo
)
from imagestore.qiniu_manager import(
    get_extension,
    handle_uploaded_file,
    upload,
    url,
)
from settings import (
    BACK_PAGE_COUNT, FILED_CHECK_MSG,
    UPLOAD_DIR,
)
import os
import datetime
import time


@staff_member_required(login_url='/admin/login')
def list(request):
    page = request.GET.get('page', '')
    param_name = request.GET.get('param_name', '')
    param_mobile = request.GET.get('param_mobile', '')
    param_email = request.GET.get('param_email', '')
    param_begin_time = request.GET.get('param_begin_time', '')
    param_status = int(request.GET.get('param_status', -1))
    param_end_time = request.GET.get('param_end_time', '')

    param_status = int(param_status) if param_status else -1
    clients = UserInfo.objects.filter(is_del=False).order_by('-created')
    # 筛选结果集
    if param_name:
        clients = clients.filter(nickname__icontains=param_name)
    if param_mobile:
        clients = clients.filter(mobile=param_mobile)
    if param_email:
        clients = clients.filter(email=param_email)
    if param_begin_time:
        clients = clients.filter(created__gte=param_begin_time)
    if param_end_time:
        clients = clients.filter(created__lte=param_end_time)
    if param_status == 0:
        clients = clients.filter(is_valid=True)
    elif param_status == 1:
        clients = clients.filter(is_valid=False)

    paginator = Paginator(clients, BACK_PAGE_COUNT)

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = {
        'module': 'user',
        'clients': clients,
        'page': page,
        'param_name': param_name,
        'param_mobile': param_mobile,
        'param_email': param_email,
        'param_begin_time': param_begin_time,
        'param_end_time': param_end_time,
        'param_status': param_status,
    }
    template = loader.get_template('super/user/list.html')
    return HttpResponse(template.render(context, request))


@staff_member_required(login_url='/admin/login')
def offline(request, userinfo_id):
    page = request.GET.get('page', '')
    param_name = request.GET.get('param_name', '')
    param_mobile = request.GET.get('param_mobile', '')
    param_email = request.GET.get('param_email', '')
    param_begin_time = request.GET.get('param_begin_time', '')
    param_status = int(request.GET.get('param_status', -1))
    param_end_time = request.GET.get('param_end_time', '')

    param_status = int(param_status) if param_status else -1

    client = UserInfo.objects.filter(pk=userinfo_id).first()
    if client:
        client.deactivate()
    return HttpResponseRedirect(reverse('web:user_list')
        + '?page=' + str(page)
        + '&param_name=' + param_name
        + '&param_mobile=' + param_mobile
        + '&param_email=' + param_email
        + '&param_begin_time=' + param_begin_time
        + '&param_status=' + str(param_status)
        + '&param_end_time=' + param_end_time
    )


@staff_member_required(login_url='/admin/login')
def online(request, userinfo_id):
    page = request.GET.get('page', '')
    param_name = request.GET.get('param_name', '')
    param_mobile = request.GET.get('param_mobile', '')
    param_email = request.GET.get('param_email', '')
    param_begin_time = request.GET.get('param_begin_time', '')
    param_status = int(request.GET.get('param_status', -1))
    param_end_time = request.GET.get('param_end_time', '')

    param_status = int(param_status) if param_status else -1

    client = UserInfo.objects.filter(pk=userinfo_id).first()
    if client:
        client.activate()
    return HttpResponseRedirect(reverse('web:user_list')
        + '?page=' + str(page)
        + '&param_name=' + param_name
        + '&param_mobile=' + param_mobile
        + '&param_email=' + param_email
        + '&param_begin_time=' + param_begin_time
        + '&param_status=' + str(param_status)
        + '&param_end_time=' + param_end_time
    )
