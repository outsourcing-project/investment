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
    ExpertTeam,
)
import datetime
import logging
import hashlib

from wechat.constants import WECHAT_BATCHGET_MATERIAL


def create_send_email_html(project_id):

    project = Project.objects.get(pk=project_id)

    html = u'<html><body><h1>' + project.name + u'</h1>' + \
            u'<table>' + \
              u'<tbody>' + \
                  u'<tr>' + \
                    u'<td>项目名称</td>' + \
                    u'<td>' + project.name + u'</td>' + \
                  u'</tr>' + \
                  u'<tr>' + \
                    u'<td>主控主题</td>' + \
                    u'<td>' + project.theme + u'</td>' + \
                  u'</tr>' + \
                  u'<tr>' + \
                    u'<td>项目总投资</td>' + \
                    u'<td>¥' + str(project.total_amount) + u'</td>' + \
                  u'</tr>' + \
                  u'<tr>' + \
                    u'<td>投资份额</td>' + \
                    u'<td>' + str(project.share_amount) + u'%</td>' + \
                  u'<tr>' + \
                    u'<td>投资周期</td>' + \
                    u'<td>' + str(project.cycle) + u'年</td>' + \
                  u'</tr>' + \
                  u'<tr>' + \
                    u'<td>预估回报</td>' + \
                    u'<td>' + str(project.expect_return) + u'%</td>' + \
                  u'</tr>' + \
                  u'<tr>' + \
                    u'<td>项目进度</td>' + \
                    u'<td>' + project.progress + u'</td>' + \
                  u'</tr>' + \
                  u'<tr>' + \
                    u'<td>备注</td>' + \
                    u'<td>' + project.note + u'</td>' + \
                  u'</tr>' + \
              u'</tbody>' + \
            u'</table>' +  \
            u'</body><input type="hidden" id="project_id" value="' + str(project.id) + u'"></html>'

    return html


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
        project.user_info = user_info
        project.attachment = attachment
        project.name = name
        project.theme = theme

        try:
            total_amount = total_amount.replace('%', '')
            share_amount = share_amount.replace('%', '')
            project.total_amount = float(total_amount) if total_amount else 0
            project.share_amount = float(share_amount) if share_amount else 0
            project.cycle = float(cycle) if cycle else 0
            project.expect_return = float(
                expect_return) if expect_return else 0
        except Exception as e:
            pass

        project.progress = progress
        project.note = note
        project.save()
        # 成功则发送邮件
        project_title = project.name
        # 获取专家团邮箱
        expert_team_list = ExpertTeam.obs.get_queryset().filter(
            is_valid=True
        )
        emails = [et.email for et in expert_team_list]
        to_addr = emails

        context = create_send_email_html(project.id)
        attach_url = project.attachment.file
        file_name = project.attachment.title

        from common.emailutils import emailutils
        emailutils.send_mail(project_title, to_addr, context, attach_url, file_name)
        project.expert_team_email = ','.join(to_addr)
        project.save()
        return HttpResponseRedirect(reverse('h5:h5_index'))

    context = {
        'user_info': user_info,
        'attachment': attachment
    }
    return render(request, "h5/publish.html", context)


def detail(request, project_id):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()
    project = Project.objects.get(pk=project_id)
    project.read_count += 1
    project.save()

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
