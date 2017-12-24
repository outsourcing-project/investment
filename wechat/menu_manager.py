# coding: utf-8

from __future__ import unicode_literals
import requests
import copy
import simplejson
from wechat.base_manager import BaseManager
from wechat.constants import GET,POST


WECHAT_MENU_CREATE_URL = 'https://api.weixin.qq.com/cgi-bin/menu/create?access_token={}'
WECHAT_MENU_CREATE_CONDITIONAL_URL = 'https://api.weixin.qq.com/cgi-bin/menu/addconditional?access_token={}'
WECHAT_MENU_DELETE_URL = 'https://api.weixin.qq.com/cgi-bin/menu/delete?access_token={}'
WECHAT_MENU_DELETE_CONDITIONAL_URL = 'https://api.weixin.qq.com/cgi-bin/menu/delconditional?access_token={}'
WECHAT_MENU_QUERY_URL = 'https://api.weixin.qq.com/cgi-bin/menu/get?access_token={}'


class MenuManager(BaseManager):

    instance = None

    def __init__(self):
        super(MenuManager, self).__init__()

    @staticmethod
    def get_instance():
        if MenuManager.instance is None:
            MenuManager.instance = MenuManager()

        return MenuManager.instance

    def create(self, menus):
        access_token = self.get_token()
        obj = self.wx_request(POST, WECHAT_MENU_CREATE_URL.format(
            access_token
        ), data=simplejson.dumps(menus, ensure_ascii=False).encode('utf-8'))

        return True

    def create_conditional(self, menus, rule):
        access_token = self.get_token()

        data = copy.deepcopy(menus)
        data.update({
            'matchrule': rule
        })

        obj = self.wx_request(POST, WECHAT_MENU_CREATE_CONDITIONAL_URL.format(
            access_token
        ), data=simplejson.dumps(data, ensure_ascii=False).encode('utf-8'))

        return True

    def delete(self):
        access_token = self.get_token()
        self.wx_request(POST, WECHAT_MENU_DELETE_URL.format(
            access_token
        ))

        return True

    def delete_conditional(self, id):
        access_token = self.get_token()
        self.wx_request(
            POST,
            WECHAT_MENU_DELETE_CONDITIONAL_URL.format(access_token),
            data=simplejson.dumps({
                'matchrule': {
                    'group_id': id,
                }
            }, ensure_ascii=False).encode('utf-8'))

        return True

    def get(self):
        access_token = self.get_token()
        obj = self.wx_request(GET, WECHAT_MENU_QUERY_URL.format(
                access_token
                ))

        return obj


menu_manager = MenuManager.get_instance()
