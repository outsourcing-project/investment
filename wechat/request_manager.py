# coding: utf-8

import requests
import simplejson as json

from .access_token_manager import access_token_manager


class RequestManager(object):

    def __init__(self):
        """
        init the RequestManager

        :param AccessTokenManager access_token_manager: 参数是 AccessTokenManager 对象
        """

        self.access_token_manager = access_token_manager

    def request(self, method, raw_url, *args, **kwargs):
        """
        发送请求
        :param str method: 请求方式
        :param str raw_url: 未拼接 access_token 的 url 字符串
        :retrun object obj: 正确时返回 obj
        """
        obj = self.request_wrap(method, raw_url, *args, **kwargs)
        errcode = obj.get('errcode', None)

        if errcode and errcode == 40001:
            # 第2次请求
            self.access_token_manager.refresh_token()
            obj = self.request_wrap(method, raw_url, *args, **kwargs)
            errcode = obj.get('errcode', None)

            if errcode and errcode == 40001:
                raise Exception('errcode:{}, errmsg:{}'.format(
                    obj.get('errcode', ''),
                    obj.get('errmsg', ''),
                ))

        return obj

    def request_wrap(self, method, raw_url, *args, **kwargs):
        """
        发送请求
        :param str method: 请求方式
        :param str raw_url: 未拼接 access_token 的 url 字符串
        :retrun object obj: 正确时返回 obj
        """
        if not method.lower() == 'post' and not method.lower() == 'get':
            raise Exception('method:{}'.format(method))
        fn = getattr(requests, method.lower())
        r = fn(raw_url.format(self.access_token_manager.get_token()), *args, **kwargs)
        obj = r.json()
        errcode = obj.get('errcode', None)

        if errcode and errcode != 40001:
            raise Exception('errcode:{}, errmsg:{}'.format(
                obj.get('errcode', ''),
                obj.get('errmsg', ''),
            ))

        return obj

    def post(self, raw_url, *args, **kwargs):
        """
        对request的简单封装，发送POST请求

        :param str raw_url: 未拼接 access_token 的 url 字符串
        :retrun object obj: 正确时返回 obj
        """
        if 'json' in kwargs:
            kwargs['json'] = json.dumps(kwargs['json'], ensure_ascii=False).encode('utf-8')
            kwargs['data'] = kwargs.pop('json')
        return self.request('post', raw_url, *args, **kwargs)

    def get(self, raw_url, *args, **kwargs):
        """
        对request的简单封装，发送GET请求

        :param str raw_url: 未拼接 access_token 的 url 字符串
        :retrun object obj: 正确时返回 obj
        """

        return self.request('get', raw_url, *args, **kwargs)


request_manager = RequestManager()
