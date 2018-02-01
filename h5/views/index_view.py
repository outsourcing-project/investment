# coding: utf-8

import requests
import urllib

from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.template import loader
from wechatpy.replies import ArticlesReply
from wechatpy.utils import ObjectDict
import requests
from settings import (
    WECHAT_APP_ID,
    WECHAT_APP_SECRET,
    DOMAIN,
)
from h5.utils import check_login
from django.views.decorators.csrf import csrf_exempt
from wechat.wx_config import get_wx_config
from wechat.template_message_manager import template_message_manager
from wechat.customer_service_manager import CustomerServiceManager
from wechat.base_manager import BaseManager
from wechat.menu_manager import menu_manager
from django.contrib.auth.models import User
from wechat.access_token_manager import access_token_manager
from wechat.request_manager import RequestManager
from web.models import (
    UserInfo,
    Project,
    InvestmentTeam,
)
from wechatpy import parse_message
from wechatpy.replies import TextReply
import datetime
import logging
import hashlib
import wechatpy
from wechat.constants import WECHAT_BATCHGET_MATERIAL


# @check_login
def index(request):
    user_info = UserInfo.objects.filter(
        is_del=False,
        user__id=request.session.get('user_id', 0)
    ).first()
    page = request.GET.get('page', 1)
    start = (int(page) - 1) * 10
    end = start + 10
    project_count = 0

    print page

    projects = Project.obs.get_queryset().order_by('-top', '-created')
    # 定位选中分类
    if int(page) == 1:
        project_count = projects.count()
        projects = projects[:10]
    else:
        projects = projects[start:end]
        tmp = loader.get_template('h5/load-project.html')
        html = tmp.render({'projects': projects})
        # 是否有下一页
        has_next = 1 if projects else 0
        return JsonResponse({'html': html, 'has_next': has_next, 'page': page})

    context = {
        'projects': projects,
        'project_count': project_count,
        'user_info': user_info,
    }
    return render(request, "h5/index.html", context)


def sharecontent(request):
    return render(request, "h5/sharecontent.html")


@csrf_exempt
def validation(request):
    echostr = request.GET.get('echostr', '')
    context = {}
    return render(request, 'MP_verify_K3P0dE2UJny1YqEW.txt', context)


@csrf_exempt
def sign_in(request):
    # 回答推送消息
    context = {}
    logging.error('-------------------sign_in--------------------')
    return render(request, 'MP_verify_K3P0dE2UJny1YqEW.txt', context)


@csrf_exempt
def customer_service_phone(request):
    echostr = request.GET.get('echostr', '')
    context = {}
    logging.error('-------------------customer_service_phone--------------------')
    return render(request, 'MP_verify_K3P0dE2UJny1YqEW.txt', context)


@csrf_exempt
def customer_add_account(request):
    csm = CustomerServiceManager(requests)
    account = 'account1@' + WECHAT_ACCOUNT
    nickname = '客服1'
    password = '123456'
    csm.add_account(account, nickname, password)

    return HttpResponse('添加客服账号成功')


@csrf_exempt
def get_merchants(request, category_id):

    clients = []
    try:
        merchants = Merchant.objects.filter(
            is_del=False,
            is_valid=True,
            category=category_id
        )
        for m in merchants:
            clients.append({
                'id': m.id,
                'name': m.name,
            })

    except Exception as e:
        return JsonResponse({'error': 1, 'msg': '查询失败'})

    return JsonResponse({'error': 0, 'clients': clients})


@csrf_exempt
def wexin(request):
    """
    所有的消息都会先进入这个函数进行处理，函数包含两个功能，
    微信接入验证是GET方法，
    微信正常的收发消息是用POST方法。
    """
    # 这个WEIXIN_TOKEN是在测试号的配置页面中配置的，等会会讲到
    WEIXIN_TOKEN = 'investment'
    if request.method == "GET":
        logging.error(request.GET)
        logging.error('---------------wexin----------------')
        signature = request.GET.get("signature", None)
        timestamp = request.GET.get("timestamp", None)
        nonce = request.GET.get("nonce", None)
        echostr = request.GET.get("echostr", None)
        token = WEIXIN_TOKEN
        tmp_list = [token, timestamp, nonce]
        tmp_list.sort()
        tmp_str = "%s%s%s" % tuple(tmp_list)
        tmp_str = hashlib.sha1(tmp_str).hexdigest()
        if tmp_str == signature:
            return HttpResponse(echostr)
        else:
            return HttpResponse("error")

    else:
        logging.error(request.POST)
        logging.error('---------------wexin----------------')
        current_date = datetime.datetime.now()
        xml = request.body
        msg = parse_message(xml)
        content = ''
        logging.error(msg)
        if msg.type == 'event':
            pass

        if msg.type == 'text' or msg.type == 'voice':
            # 如何处理，自行处理，回复一段文本或者图文
            content = '感谢您的反馈，小编将在48小时内给您回复！'

            reply = TextReply(content=content, message=msg)
            r_xml = reply.render()
            return HttpResponse(r_xml)

        return HttpResponse('success')


def send_3_msg(openid):

    text1 = '武汉文惠通，武汉人最不容错过的文化福利！欢迎关注武汉文惠通官方服务号。恭喜您注册成功，系统赠送您100积分，请认真阅读使用手册，掌握更多获取积分的方法吧。'
    text2 = '感谢您的关注'

    request_manager = RequestManager()
    customer_service_manager = CustomerServiceManager(request=request_manager)
    customer_service_manager.send_text(user_id=openid, text=text1)
    customer_service_manager.send_text(user_id=openid, text=text2)

    media_id = get_media_id()
    if media_id:
        customer_service_manager.send_article(user_id=openid, media_id=media_id)


def send_service_article(openid):
    if not openid:
        return None
    media_id = get_media_id()
    if media_id:
        request_manager = RequestManager()
        customer_service_manager = CustomerServiceManager(request=request_manager)
        customer_service_manager.send_article(user_id=openid, media_id=media_id)


def get_media_id():
    return 'QIAwk19JrMhAVqlLiUknrNQRD10AjK8LDW8SF7TLriU'

    access_token = access_token_manager.get_token()
    data = {
        'type': 'news',
        'offset': 0,
        'count': 20,
    }
    r = requests.post(WECHAT_BATCHGET_MATERIAL.format(access_token), json=data)

    if r.encoding is None or r.encoding == 'ISO-8859-1':
        r.encoding = r.apparent_encoding

    obj = r.json()
    items = obj.get('item')

    if not items:
        return None

    target_title = u'武汉扩大文化消费试点，6100万元文化消费优惠券免费领取！'
    for item in items:
        news_items = item.get('content').get('news_item')
        title = news_items[0].get('title')

        if target_title != title:
            continue

        media_id = item.get('media_id')
        return media_id


@csrf_exempt
def flush_menus(request):
    menu_manager.delete()
    menu_manager.create({
        "button": [
            {
                "name": "扫码",
                "sub_button": [
                    {"key": "rselfmenu_0_1", "type": "scancode_push", "name": "扫码"},
                    {
                        "url": "{}/h5/venues/".format(DOMAIN), "type": "view", "name": "场馆列表"
                    },
                    {
                        "url": "{}/h5/face/qr/".format(DOMAIN), "type": "view", "name": "人脸识别"
                    },
                ]
            },
            {"key": "PONY_001", "type": "click", "name": "签到"},
            {
                "name": "我的",
                "sub_button": [
                    {
                        "url": "{}/h5/user/points/".format(DOMAIN), "type": "view", "name": "我的积分"
                    },
                    {
                        "url": "{}/h5".format(DOMAIN), "type": "view", "name": "商家列表"
                    },
                    # {
                    #     "key": "PONY_002", "type": "click", "name": "客服电话"
                    # },
                    {
                        "key": "PONY_003", "type": "click", "name": "使用手册"
                    },
                    {
                        "url": "{}/h5/user/infor_check/".format(DOMAIN), "type": "view", "name": "个人信息"
                    },
                    {
                        "url": "{}/h5/merchant/login/".format(DOMAIN), "type": "view", "name": "我是商家"
                    },
                ]
            },
        ]
    })
    return HttpResponse('更新菜单成功')
