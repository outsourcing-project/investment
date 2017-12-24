# coding: utf-8

import requests

from wechat.access_token_manager import access_token_manager


class BaseManager(object):

    def __init__(self):
        pass

    def get_token(self):
        return access_token_manager.get_token()

    # def wx_request(self, method, *args, **kwargs):
    #     fn = getattr(requests, method.lower())
    #     r = fn(*args, **kwargs)

    #     obj = r.json()
    #     errcode = obj.get('errcode', None)
    #     if errcode:
    #         if errcode == 40001 or errcode == 42001:
    #             access_token_manager.refresh_token()
    #             return self.wx_request(method, *args, **kwargs)
    #         else:
    #             raise Exception('errcode:{}, errmsg:{}'.format(
    #                 obj.get('errcode', ''),
    #                 obj.get('errmsg', ''),
    #             ))

    #     return obj

    def wx_request(self, method, *args, **kwargs):

        obj = self.wx_request_wrap(method, *args, **kwargs)
        errcode = obj.get('errcode', None)

        if errcode and errcode == 40001:
            access_token_manager.refresh_token()
            obj = self.wx_request_wrap(method, *args, **kwargs)
            errcode = obj.get('errcode', None)

            if errcode and errcode == 40001:
                raise Exception('errcode:{}, errmsg:{}'.format(
                    obj.get('errcode', ''),
                    obj.get('errmsg', ''),
                ))

        return obj

    def wx_request_wrap(self, method, *args, **kwargs):

        fn = getattr(requests, method.lower())
        r = fn(*args, **kwargs)

        obj = r.json()
        errcode = obj.get('errcode', None)

        if errcode and errcode != 40001:
            raise Exception('errcode:{}, errmsg:{}'.format(
                obj.get('errcode', ''),
                obj.get('errmsg', ''),
            ))

        return obj
