# coding: utf-8

import requests
import time

from settings import REDIS_HOST, REDIS_PORT, REDIS_DB, WECHAT_APP_ID, WECHAT_APP_SECRET as WECHAT_SECRET
import redis
import simplejson


WX_ACCESS_TOKEN_REFRESH_URL = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid={}&secret={}'


class AccessTokenManager(object):

    instance = None

    def __init__(self, app_id, app_secret):
        self.app_id = app_id
        self.app_secret = app_secret
        self.redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)

    @staticmethod
    def get_instance():
        if AccessTokenManager.instance is None:
            AccessTokenManager.instance = AccessTokenManager(WECHAT_APP_ID, WECHAT_SECRET)

        return AccessTokenManager.instance

    def refresh_token(self):
        r = requests.get(WX_ACCESS_TOKEN_REFRESH_URL.format(
            self.app_id,
            self.app_secret,
        ))

        obj = r.json()
        if obj.get('errcode', None):
            raise Exception('Failed to get the access token, code:{}'.format(obj.get('errcode')))

        expires_in = obj['expires_in']
        obj = {
            'access_token': obj['access_token'],
            'expired': int(time.time()) + expires_in,
        }

        self.redis_conn.set('temple_wechat_access_token', simplejson.dumps(obj), ex=expires_in)
        return obj

    def get_token(self):
        obj = self._get_token()
        if not obj:
            obj = self.refresh_token()

        now = int(time.time())
        if now >= obj['expired']:
            self.refresh_token()

        return obj['access_token']

    def _get_token(self):
        data = self.redis_conn.get('temple_wechat_access_token')
        if not data:
            return None

        return simplejson.loads(data)

access_token_manager = AccessTokenManager.get_instance()
