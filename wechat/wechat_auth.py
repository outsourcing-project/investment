# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from functools import wraps

from settings import DOMAIN, WECHAT_APP_ID, WECHAT_SECRET, USE_FAKE_WECHAT_USER

from .constants import WECAHT_USER_INFO_URL, WECHAT_AUTH_URL, WECHAT_GET_ACCESS_TOKEN_URL
from orange_management.models import OrangeUser

import requests
import logging


def get_data(code):
    r = requests.get(WECHAT_GET_ACCESS_TOKEN_URL.format(
        WECHAT_APP_ID, WECHAT_SECRET, code
    ))

    data = r.json()
    return data


def get_user_info(access_token, openid):
    r = requests.get(WECAHT_USER_INFO_URL.format(
        access_token, openid
    ))
    if r.encoding is None or r.encoding == 'ISO-8859-1':
        r.encoding = r.apparent_encoding
    data = r.json()
    return data


def web_webchat_check_login(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):
        if USE_FAKE_WECHAT_USER:
            make_fake_user(request)
            return view(request, *args, **kwargs)

        openid = request.session.get('openid', None)
        unionid = request.session.get('unionid', None)
        app = request.GET.get('app', '')
        if not app and (not unionid or not openid):
            request.session['red_next_url'] = request.get_raw_uri()
            return HttpResponseRedirect(WECHAT_AUTH_URL)

        return view(request, *args, **kwargs)

    return wrapper


def wechat_do_login(request):
    # 获取access_token
    data = get_data(request.GET.get('code', ''))
    openid = data.get('openid')
    access_token = data.get('access_token', '')
    if not access_token:
        return HttpResponseRedirect('/h5/login')
    user_info_data = get_user_info(access_token, openid)

    nickname = user_info_data.get('nickname', '')
    city = user_info_data.get('city', '')
    province = user_info_data.get('province', '')
    country = user_info_data.get('country', '')
    headimgurl = user_info_data.get('headimgurl', '')
    unionid = user_info_data.get('unionid', '')

    orange_user = OrangeUser.objects.filter(wx_unionid=unionid).first()
    if orange_user:
        request.session['user_id'] = orange_user.id
    request.session['nickname'] = nickname
    request.session['city'] = city
    request.session['province'] = province
    request.session['country'] = country
    request.session['avatar'] = headimgurl
    print 'wechat_do_login', unionid

    # 设置Session
    request.session['unionid'] = unionid
    request.session['openid'] = openid
    # 获取用户ip
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        user_ip = request.META['HTTP_X_FORWARDED_FOR'].split(',')[0]
    else:
        user_ip = request.META['REMOTE_ADDR']
    request.session['user_ip'] = user_ip
    red_next_url = request.session.get('red_next_url', '')
    if not red_next_url:
        red_next_url = '/h5'
    return HttpResponseRedirect(red_next_url)


def make_fake_user(request):
    unionid = 'attackt'
    mobile = '12345678901'
    orange_user, _ = OrangeUser.objects.get_or_create(wx_unionid=unionid, mobile=mobile)
    request.session['unionid'] = unionid
    request.session['user_id'] = orange_user.id
