# coding: utf-8

import requests
import urllib

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from wechat import constants
from settings import WECHAT_APP_ID, WECHAT_APP_SECRET, DOMAIN
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from web.models import UserInfo


# 微信授权
def login_wechat(request):
    if 'red_next_url' not in request.session:
        request.session['red_next_url'] = reverse('h5:index')
    redirect_url = constants.WECHAT_AUTH_URL
    return HttpResponseRedirect(redirect_url)


def login_wechat1(request):
    if 'red_next_url' not in request.session:
        request.session['red_next_url'] = reverse('h5:index')
    redirect_url = constants.WECHAT_AUTH_URL1
    return HttpResponseRedirect(redirect_url)

# 微信授权回调
def login_wechat_callback(request):
    code = request.GET.get('code', '')
    r = requests.get(constants.WECHAT_GET_ACCESS_TOKEN_URL.format(
        WECHAT_APP_ID,
        WECHAT_APP_SECRET,
        code
    ))
    data = r.json()
    # 获取请求数据 并保存
    openid = data.get('openid')
    access_token = data.get('access_token')
    request.session['openid'] = openid
    request.session['access_token'] = access_token
    # 取得登陆用户
    user_info = UserInfo.objects.filter(
        openid=openid,
        is_del=False,
        is_valid=True
    ).first()
    red_next_url = request.session.get('red_next_url', reverse('h5:index'))
    data = get_wechat_userinfo(access_token, openid)

    if user_info:
        user_info.nickname = data.get('nickname', '')
        user_info.city = data.get('city', '')
        user_info.province = data.get('province', '')
        user_info.country = data.get('country', '')
        user_info.sex = data.get('sex', 0)
        if openid:
            user_info.openid = openid
        user_info.headimgurl = data.get('headimgurl', 0)
        user_info.save()

        user = user_info.get_user()
        try:
            user.username = user_info.openid
            user.first_name = user_info.nickname
            user.save()
        except Exception as e:
            pass

        request.session['user_id'] = user_info.user.id
        return HttpResponseRedirect(red_next_url)
    else:
        if openid:
            user_info = UserInfo()
            user_info.nickname = data.get('nickname', '')
            user_info.city = data.get('city', '')
            user_info.province = data.get('province', '')
            user_info.country = data.get('country', '')
            user_info.sex = data.get('sex', 0)
            user_info.openid = openid
            user_info.headimgurl = data.get('headimgurl', 0)
            user, _ = User.objects.get_or_create(
                username=openid,
            )
            user_info.first_name = user_info.nickname
            user_info.user = user
            user_info.save()

        return HttpResponseRedirect(red_next_url)


# 获取微信登陆的用户信息<不提供外部访问>
def get_wechat_userinfo(access_token, openid):
    r = requests.post(constants.WECAHT_USER_INFO_URL.format(
        access_token, openid
    ))
    if r.encoding is None or r.encoding == 'ISO-8859-1':
        r.encoding = r.apparent_encoding
    data = r.json()
    return data
