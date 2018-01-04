# coding: utf-8

import requests
import urllib

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template import loader
import requests
from settings import (
    WECHAT_APP_ID,
    WECHAT_APP_SECRET,
    DOMAIN,
)
from h5.utils import check_login, check_user
from django.views.decorators.csrf import csrf_exempt
from wechat.wx_config import get_wx_config
from django.contrib.auth.models import User
from web.models import (
    UserInfo,
    Project,
    InvestmentTeamShow,
    Attachment,
)
import datetime
import logging
import hashlib
import random

from wechat.constants import WECHAT_BATCHGET_MATERIAL


@check_user
def index(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()
    page = request.GET.get('page', 1)
    start = (int(page) - 1) * 7
    end = start + 7
    project_count = 0

    projects = Project.obs.get_queryset().filter().order_by('-top', '-created')

    context = {
        'projects': projects,
        'user_info': user_info,
    }
    return render(request, "h5/personal.html", context)


@check_user
def person_info(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()

    context = {
        'user_info': user_info,
    }

    return render(request, "h5/person_info.html", context)


def login(request):

    msg = ''
    team_show_list = InvestmentTeamShow.obs.get_queryset().order_by('-order_no')

    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        code = request.POST.get('code', '')

        if code != '6666':
            msg = '验证码错误'
        else:
            user, _ = User.objects.get_or_create(
                username=phone,
            )
            user_info = UserInfo.objects.get_or_create(
                user=user,
                mobile=phone
            )
            request.session['user_id'] = user.id
            return HttpResponseRedirect(reverse('h5:user_index'))

    context = {
        'team_show_list': team_show_list,
        'msg': msg,
    }

    return render(request, "h5/login.html", context)


def login_out(request):
    if request.session.get('user_id'):
        del request.session['user_id']
    return HttpResponseRedirect(reverse('h5:h5_index'))


def bang_email(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()
    msg = ''
    # 判断是否已绑定过邮箱
    if not user_info:
        return HttpResponseRedirect(reverse('h5:login'))
    elif user_info.email:
        return HttpResponseRedirect(reverse('h5:send_email'))

    if request.method == 'POST':
        email = request.POST.get('email', '')
        username = request.POST.get('username', '')

        user_info.email = email
        user_info.user_name = username
        user_info.save()
        return HttpResponseRedirect(reverse('h5:send_email'))

    context = {
        'msg': msg,
    }

    return render(request, "h5/edit_phone.html", context)


def send_email(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()
    if not user_info:
        return HttpResponseRedirect(reverse('h5:login'))
    elif not user_info.email:
        return HttpResponseRedirect(reverse('h5:bang_email'))

    context = {
        'user_info': user_info,
    }

    return render(request, "h5/send_email.html", context)


@check_user
def edit_uname(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()
    if request.method == 'POST':
        username = request.POST.get('username', '')

        user_info.user_name = username
        user_info.save()
        return HttpResponseRedirect(reverse('h5:person_info'))

    context = {
        'user_info': user_info,
    }

    return render(request, "h5/edit_person.html", context)


@check_user
def edit_email(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()

    if request.method == 'POST':
        email = request.POST.get('email', '')

        user_info.email = email
        user_info.save()
        return HttpResponseRedirect(reverse('h5:person_info'))

    context = {
        'user_info': user_info,
    }
    return render(request, "h5/edit_email.html", context)


@check_user
def edit_mobile(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()

    msg = ''
    if request.method == 'POST':
        code = request.POST.get('code', '')

        if code != '6666':
            msg = '验证码错误'
        else:
            return HttpResponseRedirect(
                reverse(
                    'h5:confirm_mobile'))

    context = {
        'user_info': user_info,
        'msg': msg,
    }
    return render(request, "h5/get_verify.html", context)


@check_user
def confirm_mobile(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()

    msg = ''
    if request.method == 'POST':
        phone = request.POST.get('phone', '')
        code = request.POST.get('code', '')
        if code != '6666':
            msg = '验证码错误'
        else:
            user_info.mobile = phone
            user_info.save()
            return HttpResponseRedirect(reverse('h5:user_index'))

    context = {
        'user_info': user_info,
        'msg': msg,
    }
    return render(request, "h5/edit_phone2.html", context)


@check_user
def attachment(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()

    attachment_list = Attachment.obs.get_queryset().filter(
        user_info=user_info
    ).order_by('-created')
    context = {
        'attachment_list': attachment_list,
        'user_info': user_info
    }
    return render(request, "h5/my_file.html", context)


@check_user
def project(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()

    project_list = Project.obs.get_queryset().filter(user_info=user_info)

    context = {
        'user_info': user_info,
        'project_list': project_list,
    }
    return render(request, "h5/myproject.html", context)


@check_user
def about(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()

    context = {
        'user_info': user_info,
    }
    return render(request, "h5/about.html", context)
