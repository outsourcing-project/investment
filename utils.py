# coding: utf-8

from rest_framework_jwt.settings import api_settings
from settings import SMS_ACCOUNT_SID, SMS_ACCOUNT_TOKEN, SMS_SUB_ACCOUNT_SID, SMS_TEMPLATE_CODE_ID, SMS_SUB_ACCOUNT_TOKEN, SMS_APP_ID
from sms import SMSManager
from django.core.urlresolvers import reverse
from functools import wraps
from django.http import HttpResponseRedirect

import random
import simplejson
import time
import math
import string
import logging
import hashlib
import uuid


def _uuid():
    uid = str(uuid.uuid1())
    child_list = uid.split('-')[:-1]
    return ''.join(child_list)


# 产生唯一订单号
def generate_order_num():
    return _uuid()


def website_check_login(view):
    @wraps(view)
    def wrapper(request, *args, **kwargs):

        c_user = request.session.get('c_user', None)
        if not c_user:
            return HttpResponseRedirect(reverse('website:home_login'))

        return view(request, *args, **kwargs)

    return wrapper

def md5_create(src):
    """生成md5字符串
    """
    m2 = hashlib.md5()
    m2.update(src)
    return m2.hexdigest()


def jwt_token_gen(user):
    jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
    jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

    payload = jwt_payload_handler(user)
    token = jwt_encode_handler(payload)

    return token


def jwt_token_decode(token):
    jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

    payload = jwt_decode_handler(token)

    return payload


def send_v_code(mobile, v_code, expired_minutes):
    sms_manager = SMSManager(SMS_ACCOUNT_SID, SMS_ACCOUNT_TOKEN, SMS_SUB_ACCOUNT_SID, SMS_SUB_ACCOUNT_TOKEN, SMS_APP_ID)
    try:
        result = sms_manager.send_auth_code(mobile, v_code, expired_minutes=expired_minutes, template_id=SMS_TEMPLATE_CODE_ID)
        send_status = True
    except Exception, e:
        send_status = False
    data = {}
    if send_status:
        data['mobile'] = mobile
        data['v_code'] = v_code
        data['send_time'] = int(time.time())
    return data


def send_notice(mobile, datas, template_id):
    sms_manager = SMSManager(SMS_ACCOUNT_SID, SMS_ACCOUNT_TOKEN, SMS_SUB_ACCOUNT_SID, SMS_SUB_ACCOUNT_TOKEN, SMS_APP_ID)
    try:
        result = sms_manager.send_sms_msg(mobile, datas, 2, template_id)
        send_status = True
    except Exception, e:
        send_status = False
    data = {}
    if send_status:
        data['mobile'] = mobile
        data['send_time'] = int(time.time())
    return data


def send_voice_code(mobile, v_code):
    sms_manager = SMSManager(SMS_ACCOUNT_SID, SMS_ACCOUNT_TOKEN, SMS_SUB_ACCOUNT_SID, SMS_SUB_ACCOUNT_TOKEN, SMS_APP_ID)
    try:
        result = sms_manager.send_voice_code(mobile, v_code)
        send_status = True
    except Exception, e:
        send_status = False
    data = {}
    if send_status:
        data['mobile'] = mobile
        data['v_code'] = v_code
        data['send_time'] = int(time.time())
    return data


def check_v_code(request, redis_conn, mobile, v_code, expired_minutes):
    # 返回值0，1，2，3，0代表验证通过，1代表验证码过期，2代表验证码错误，3代表未发送验证码
    if redis_conn.get('v_code_json'):
        v_data = redis_conn.get('v_code_json')
        v_data = simplejson.loads(v_data)
        s_v_code = v_data.get(mobile, '')
        if s_v_code and s_v_code == v_code:
            diff_v_time = int(time.time())-int(v_data['send_time'])
            if diff_v_time <= int(expired_minutes)*60:
                return 0
            elif diff_v_time > int(expired_minutes)*60:
                return 1
        else:
            return 2
    else:
        return 3

def verify_mobile(mobile):
    # 返回值True 代表验证通过
    try:
        v_nmuber = int(mobile)

        if len(str(v_nmuber)) == 11:
            # pre_v_nmuber = int(str(v_nmuber)[0:3])
            # cnm = pre_v_nmuber in cn_mobile
            # cnu = pre_v_nmuber in cn_union
            # cnt = pre_v_nmuber in cn_telecom

            # if cnm or cnu or cnt:
            return True
        return False
    except Exception, e:
        return False
