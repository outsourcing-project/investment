# coding: utf-8

import requests
import time

from .access_token_manager import access_token_manager
from .base_manager import BaseManager
from .constants import GET, POST


WX_JSAPI_TICKET_REFRESH_URL = 'https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token={}&type=jsapi'


class JsapiTicketManager(BaseManager):

    instance = None

    def __init__(self):
        super(JsapiTicketManager, self).__init__()
        self.jsapi_ticket = None
        self.expired = -1

    @staticmethod
    def get_instance():
        if JsapiTicketManager.instance is None:
            JsapiTicketManager.instance = JsapiTicketManager()

        return JsapiTicketManager.instance

    def refresh_ticket(self):
        access_token = self.get_token()
        obj = self.wx_request(GET, WX_JSAPI_TICKET_REFRESH_URL.format(
            access_token
        ))

        if obj.get('errcode', None):
            raise Exception('Failed to get the jsapi ticket, code:{}'.format(obj.get('errcode')))

        self.expired = int(time.time()) + obj['expires_in']
        self.jsapi_ticket = obj['ticket']

    def get_ticket(self):
        now = int(time.time())
        if now >= self.expired:
            self.refresh_ticket()

        return self.jsapi_ticket

jsapi_ticket_manager = JsapiTicketManager.get_instance()
