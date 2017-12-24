# coding: utf-8

import time
import hashlib
import os

from .jsapi_ticket_manager import jsapi_ticket_manager
from settings import WECHAT_APP_ID as appId

STRING_1 = 'jsapi_ticket={}&noncestr={}&timestamp={}&url={}'


def get_wx_config(url):
    jsapi_ticket = jsapi_ticket_manager.get_ticket()
    noncestr = ''.join(map(lambda xx: (hex(ord(xx))[2:]), os.urandom(8)))
    timestamp = int(time.time())

    string1 = STRING_1.format(jsapi_ticket, noncestr, timestamp, url)
    sha1 = hashlib.sha1()
    sha1.update(string1)
    signature = sha1.hexdigest()

    return {
        'appId': appId,
        'timestamp': timestamp,
        'noncestr': noncestr,
        'signature': signature,
        'string_1': string1
    }
