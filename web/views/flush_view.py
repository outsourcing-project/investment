# coding: utf-8

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from web.models import (
    Setting,
)
from common.lookup import setting_config
import datetime


@staff_member_required(login_url='/admin/login')
def topic(request):
    topics = Topic.objects.filter(status=0)
    for topic in topics:
        if datetime.date.today() > topic.end_date:
            topic.status = 1
            topic.save()
    return render(request, 'super/flush.html')


@staff_member_required(login_url='/admin/login')
def setting(request):
    for c in setting_config:
        setting, _ = Setting.objects.get_or_create(name=c['name'], code=c['code'])
        setting.value = c['value']
        setting.save()

    return render(request, 'super/flush.html')
