# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from imagestore.qiniu_manager import (
    get_extension,
    handle_uploaded_file,
)
from settings import(
    UPLOAD_DIR,
)
import os
import datetime
import time
import simplejson
import requests
import random
import string
import logging


@staff_member_required(login_url='/admin/login')
def index(request):

    context = {
        'module': 'index',
    }

    return render(request, 'super/index.html', context)

@csrf_exempt
def ckeditor_upload(request):
    if request.FILES:
        ts = int(time.time())
        img_file = request.FILES.get('upload', '')

        checkNum = request.GET.get('CKEditorFuncNum', '')
        ext = get_extension(request.FILES['upload'].name)
        key = 'ckeditor_{}.{}'.format(ts, ext)

        handle_uploaded_file(img_file, key)
        # 上传图片到qiniu
        upload(key, os.path.join(UPLOAD_DIR, key))
        return HttpResponse("<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction(\
            '"+checkNum+"','"+url(key)+"','')</script>")


@csrf_exempt
def ckeditor_many_upload(request):
    if request.FILES:
        ts = int(time.time())
        img_file = request.FILES.get('upload', '')

        checkNum = request.GET.get('CKEditorFuncNum', '')
        ext = get_extension(request.FILES['upload'].name)
        random_num = ''.join([random.choice(string.digits) for _ in range(4)])
        key = 'ckeditor_many_{}_{}.{}'.format(ts, random_num, ext)

        handle_uploaded_file(img_file, key)
        # 上传图片到qiniu
        upload(key, os.path.join(UPLOAD_DIR, key))
        return JsonResponse({'uploaded': 1, 'fileName': key, 'url': url(key)})


@csrf_exempt
def ckeditor_upload(request):
    if request.FILES:
        checkNum = request.GET.get('CKEditorFuncNum')

        upload_img = request.FILES['upload']
        new_file_name = get_no_repeat_s() + '.jpg'

        fh = open(UPLOAD_DIR + '/' + new_file_name, 'wb')
        fh.write(upload_img.read())
        fh.close()
        upload(new_file_name, os.path.join(UPLOAD_DIR, new_file_name))
        picture_url = url(new_file_name)
        # 上传图片到qiniu
        return HttpResponse("<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction(\
            '" + checkNum + "','" + picture_url + "','')</script>")


def uptoken(request):
    now = datetime.datetime.now()
    key = now.strftime('%Y%m%d%H%M%S%s')

    token = get_upload_token(key)
    return HttpResponse(simplejson.dumps({
        'uptoken': token,
    }))

