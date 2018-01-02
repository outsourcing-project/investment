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
    Attachment,
)
import datetime
import logging
import hashlib

from wechat.constants import WECHAT_BATCHGET_MATERIAL


@check_user
def create(request, attachment_id):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()
    attachment = Attachment.objects.get(pk=attachment_id)
    if request.method == 'POST':
        name = request.POST.get('name', '')
        theme = request.POST.get('theme', '')
        total_amount = request.POST.get('total_amount', 0)
        share_amount = request.POST.get('share_amount', 0)
        cycle = request.POST.get('cycle', 0)
        expect_return = request.POST.get('expect_return', 0)
        attachment_id = request.POST.get('attachment_id', 0)
        progress = request.POST.get('progress', '')
        note = request.POST.get('note', '')

        project = Project()
        project.attachment = attachment
        project.name = name
        project.theme = theme
        try:
            project.total_amount = float(total_amount) if total_amount else 0
            project.share_amount = float(share_amount) if share_amount else 0
            project.cycle = float(cycle) if cycle else 0
            project.expect_return = float(expect_return) if expect_return else 0
        except Exception as e:
            pass

        project.progress = progress
        project.note = note
        project.save()
        return HttpResponseRedirect(reverse('h5:h5_index'))

    context = {
        'user_info': user_info,
        'attachment': attachment
    }
    return render(request, "h5/publish.html", context)

@check_user
def detail(request, project_id):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()
    project = Project.objects.get(pk=project_id)

    context = {
        'user_info': user_info,
        'project': project,
    }
    return render(request, "h5/project_detail.html", context)


@check_user
def attachment(request, attachment_id):
    attachment = Attachment.objects.get(pk=attachment_id)

    context = {
        'attachment': attachment,
    }
    return render(request, "h5/pdf.html", context)

