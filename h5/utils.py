# coding: utf-8
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from functools import wraps
from django.contrib.auth.models import User
from settings import UPLOAD_DIR, DOMAIN

import random
import os
import hashlib
import string
import sys
sys.setrecursionlimit(3000)


from math import radians, cos, sin, asin, sqrt


def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1 = float(lon1)
    lat1 = float(lat1)
    lon2 = float(lon2)
    lat2 = float(lat2)
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return round(c * r * 1000, 1)


def check_login(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        user_id = request.session.get('user_id', 0)
        user = User.objects.filter(pk=user_id).first()
        if not user_id or not user:
            if user_id:
                del request.session['user_id']
            request.session['red_next_url'] = request.get_raw_uri()
            return HttpResponseRedirect(reverse('h5:login_wechat'))

        return view(request, *args, **kwargs)

    return wrapper


def check_user(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        # 是否有发过附件
        is_send_file = True
        user_id = request.session.get('user_id', 0)
        user = User.objects.filter(pk=user_id).first()
        if not user or not user.userinfo.mobile:
            request.session['red_next_url'] = request.get_raw_uri()
            return HttpResponseRedirect(reverse('h5:login'))
        elif not user.userinfo.email:
            request.session['red_next_url'] = request.get_raw_uri()
            return HttpResponseRedirect(reverse('h5:bang_email'))
        elif not is_send_file:
            request.session['red_next_url'] = request.get_raw_uri()
            return HttpResponseRedirect(reverse('h5:send_email'))

        return view(request, *args, **kwargs)

    return wrapper


def md5_create(src):
    """生成md5字符串
    """
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()
