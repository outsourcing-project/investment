# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

from settings import UPLOAD_DIR, DOMAIN, WECHAT_PAY_MCH_KEY, WECHAT_APP_ID, WECHAT_APP_SECRET, WECHAT_MCH_ID
from .wx_config import get_wx_config

import simplejson
import logging
import os
import datetime
import time
import hashlib
import random
import requests
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape
import sys
reload(sys)
sys.setdefaultencoding("utf-8")


@csrf_exempt
def wx_create_order(body, detail, out_trade_no, product_id, openid, spbill_create_ip, total_fee):
    total_fee = str(int(total_fee*100))
    noncestr = ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(8)))
    stringA = "appid=" + WECHAT_APP_ID + "&body=" + body + "&detail=" + detail +  "&device_info=WEB&mch_id=" + WECHAT_MCH_ID + "&nonce_str=" + noncestr + "&notify_url=" + DOMAIN + "/h5/wx_callback_pay/&openid=" +openid + "&out_trade_no=" + out_trade_no + "&product_id=" + product_id + "&spbill_create_ip=" + spbill_create_ip + "&total_fee=" + total_fee + "&trade_type=JSAPI"
    stringSignTemp = stringA + "&key=" + WECHAT_PAY_MCH_KEY
    sign = hashlib.md5(stringSignTemp.encode('utf-8')).hexdigest().upper()
    # 生成订单
    xml_request = "<xml>\
                       <appid>" + WECHAT_APP_ID + "</appid>\
                       <body>" + body + "</body>\
                       <detail>" + detail + "</detail>\
                       <device_info>WEB</device_info>\
                       <mch_id>" + WECHAT_MCH_ID + "</mch_id>\
                       <nonce_str><![CDATA[" + noncestr + "]]></nonce_str>\
                       <notify_url><![CDATA[" + DOMAIN + "/h5/wx_callback_pay/]]></notify_url>\
                       <openid><![CDATA[" + openid + "]]></openid>\
                       <out_trade_no><![CDATA[" + out_trade_no + "]]></out_trade_no>\
                       <product_id>" + product_id + "</product_id>\
                       <spbill_create_ip><![CDATA[" + spbill_create_ip + "]]></spbill_create_ip>\
                       <total_fee>" + total_fee + "</total_fee>\
                       <trade_type>JSAPI</trade_type>\
                       <sign><![CDATA[" + sign + "]]></sign>\
                    </xml>"


    r = requests.post('https://api.mch.weixin.qq.com/pay/unifiedorder', data=xml_request.encode('utf-8'))
    if r.encoding is None or r.encoding == 'ISO-8859-1':
        r.encoding = r.apparent_encoding
    logging.error(r.text)
    root = ET.fromstring(r.text)
    # 解析xml内容
    for child in root:
        if child.tag == 'return_code':
            return_code = child.text
        if child.tag == 'return_msg':
            return_msg = child.text
        if child.tag == 'result_code':
            result_code = child.text
        if child.tag == 'trade_type':
            trade_type = child.text
        if child.tag == 'prepay_id':
            prepay_id = child.text

    if return_code == 'SUCCESS' and result_code == 'SUCCESS':
        # 成功需要修改订单状态
        timestamp = str(int(time.time()))
        stringB = "appId=" + WECHAT_APP_ID + "&nonceStr=" + noncestr + "&package=prepay_id=" + prepay_id + "&signType=MD5&timeStamp=" + timestamp
        stringSignTempB = stringB + "&key=" + WECHAT_PAY_MCH_KEY
        signB = hashlib.md5(stringSignTempB.encode('utf-8')).hexdigest().upper()
        wx_pay_json = {'timestamp': timestamp, 'nonceStr': noncestr, 'signType': 'MD5', 'prepay_id': prepay_id, 'paySign': signB, 'out_trade_no': out_trade_no}
        return {'error_code': 0, 'msg': '下单成功', 'wx_pay_json': wx_pay_json}
    else:
        return {'error_code': 1, 'msg': '下单失败', 'xml_request': xml_request, 'stringSignTemp': stringSignTemp}


# 支付成功后微信回调地址
@csrf_exempt
def wx_callback_pay(xml_read):
    root = ET.fromstring(xml_read)
    # 解析xml内容
    for child in root:
        if child.tag == 'return_code':
            return_code = child.text
        if child.tag == 'result_code':
            result_code = child.text
        if child.tag == 'out_trade_no':
            out_trade_no = child.text
    if return_code == 'SUCCESS' and result_code == 'SUCCESS':
        return out_trade_no
    else:
        return 0

