# coding: utf-8

from wechat.base_manager import BaseManager

from constants import (
    CUSTOMER_SERVICE_CREATE_ACCOUNT_URL,
    CUSTOMER_SERVICE_UPDATE_ACCOUNT_URL,
    CUSTOMER_SERVICE_DELETE_ACCOUNT_URL,
    CUSTOMER_SERVICE_SET_HEADIMG_URL,
    CUSTOMER_SERVICE_GET_ACCOUNT_LIST_URL,
    CUSTOMER_SERVICE_SEND_MESSAGE_URL,
)

class CustomerServiceManager(BaseManager):

    def __init__(self, request, customer_service_account=None):
        """
        初始化

        :param RequestManager request: RequestManager类的实例
        :param str customer_service_account: 客服账号, 拥有头像与昵称
        """
        self.request_manager = request
        self.customer_service_account = customer_service_account

    def _manage_account(self, account, nickname, password, create=False, delete=False):
        access_token = self.get_token()
        """
        管理客服账号(创建、修改、删除)

        :param str account: 完整客服账号, 格式为: 账号前缀@公众号微信号
        :param str nickname: 客服昵称, 最长6个汉字或12个英文字符
        :param str password: 客服登陆密码, 格式为密码明文的32位加密MD5值
                             该密码仅用于多客服功能, 若不使用多客服功能, 则不必设置密码
        :param bool create: 默认False, 为True时创建账号
        :param bool delete: 默认False, 为True时删除账号
        :return: 成功时返回True
        """
        account_data = {
            'kf_account': account,
            'nickname': nickname
        }
        if password:
            account_data['password'] = password

        url = CUSTOMER_SERVICE_UPDATE_ACCOUNT_URL
        if delete:
            url = CUSTOMER_SERVICE_DELETE_ACCOUNT_URL
        if create:
            url = CUSTOMER_SERVICE_CREATE_ACCOUNT_URL
        if create and delete:
            raise Exception('创建、删除命令冲突')

        response = self.request_manager.post(
            url.format(access_token),
            data=account_data
        )

        clean_data = {
            'errcode': response['errcode'],
            'errmsg': response['errmsg'],
        }

        return True

    def add_account(self, account, nickname, password=None):
        """
        添加客服账号

        :param str account: 完整客服账号, 格式为: 账号前缀@公众号微信号
        :param str nickname: 客服昵称, 最长6个汉字或12个英文字符
        :param str password: 客服登陆密码, 格式为密码明文的32位加密MD5值
                             该密码仅用于多客服功能, 若不使用多客服功能, 则不必设置密码
        :return: 成功时返回True
        """
        return self._manage_account(account, nickname, password, create=True)

    def update_account(self, account, nickname, password=None):
        """
        修改客服账号

        :param str account: 完整客服账号, 格式为: 账号前缀@公众号微信号
        :param str nickname: 客服昵称, 最长6个汉字或12个英文字符
        :param str password: 客服登陆密码, 格式为密码明文的32位加密MD5值
                             该密码仅用于多客服功能, 若不使用多客服功能, 则不必设置密码
        :return: 成功时返回True
        """
        return self._manage_account(account, nickname, password)

    def del_account(self, account, nickname, password=None):
        """
        删除客服账号

        :param str account: 完整客服账号, 格式为: 账号前缀@公众号微信号
        :param str nickname: 客服昵称, 最长6个汉字或12个英文字符
        :param str password: 客服登陆密码, 格式为密码明文的32位加密MD5值
                             该密码仅用于多客服功能, 若不使用多客服功能, 则不必设置密码
        :return: 成功时返回True
        """
        return self._manage_account(account, nickname, password, delete=True)

    def set_headimg(self, headimg_file, customer_service_account=None):
        """
        设置客服头像

        :param file headimg_file: 头像图片文件(二进制打开), 头像图片文件必须是jpg格式, 推荐使用640*640大小的图片以达到最佳效果
        :param str customer_service_account: 客服账号
        :return: 成功时返回True
        """
        if not customer_service_account and self.customer_service_account:
            customer_service_account = self.customer_service_account

        if customer_service_account:
            url = ''.join([
                CUSTOMER_SERVICE_SET_HEADIMG_URL,
                '&kf_account=',
                customer_service_account
            ])
            files_data = {
                'file': headimg_file,
            }
            response = self.request_manager.post(
                raw_url=url,
                files=files_data
            )
            clean_data = {
                'errcode': response['errcode'],
                'errmsg': response['errmsg'],
            }
            return True
        else:
            raise Exception('未指定客服账号')

    def _clean_account_info(self, account_info):
        """
        整理客服账号数据

        :param dict account_info: 客服账号数据
        {
            "kf_account": "test1@test",
            "kf_nick": "ntest1",
            "kf_id": "1001",
            "kf_headimgurl": "http://mmbiz.qpic.cn/mmbiz/4whpV1VZl2iccsvN0Yb...ILcibPoEGb2fPfEOmw/0",
        }
        :return: 整理之后的客服账号数据
        {
            "account": "test1@test",
            "nickname": "ntest1",
            "account_id": "1001",
            "headimg_url": "http://mmbiz.qpic.cn/mmbiz/4whpV1VZl2iccsvN0Yb...ILcibPoEGb2fPfEOmw/0",
        }
        :rtype: dict
        """
        return {
            'account': account_info['kf_account'],
            'nickname': account_info['kf_nick'],
            'account_id': account_info['kf_id'],
            'headimg_url': account_info['kf_headimgurl'],
        }

    def get_account_list(self):
        """
        获取所有客服账号的基本信息,包括客服工号、客服昵称、客服登陆账号、客服头像

        :return: 客服账号信息列表
        [
            {
                "account": "test1@test",
                "nickname": "ntest1",
                "account_id": "1001",
                "headimg_url": "http://mmbiz.qpic.cn/mmbiz/4whpV1VZl2iccsvN0Yb...ILcibPoEGb2fPfEOmw/0",
            },
            {
                "account": "test2@test",
                "nickname": "ntest2",
                "account_id": "1002",
                "headimg_url": "http://mmbiz.qpic.cn/mmbiz/4whpV1VZl2iccsv8vYb...cibEGbahs2fPfEOmw/0",
            },
        ]
        :rtype: list
        """
        response = self.request_manager.get(
            CUSTOMER_SERVICE_GET_ACCOUNT_LIST_URL,
        )
        account_list = response['kf_list']
        clean_account_list = []
        for account in account_list:
            clean_account_list.append(self._clean_account_info(account))
        return clean_account_list

    def send_message(self, data):
        """
        发送信息

        :param dict data: 待发送的数据包
        :return: 发送成功时返回True
        """
        if self.customer_service_account:
            data['customservice'] = {
                'kf_account': self.customer_service_account,
            }
        response = self.request_manager.post(
            raw_url=CUSTOMER_SERVICE_SEND_MESSAGE_URL,
            json=data,
        )
        clean_data = {
            'errcode': response['errcode'],
            'errmsg': response['errmsg'],
        }
        return True

    def send_text(self, user_id, text):
        """
        发送文本消息

        :param str user_id: 发送对象的ID
        :param str text: 发送内容(文本形式)
        :return: 发送成功时返回True
        """
        data = {
            'touser': user_id,
            'msgtype': 'text',
            'text': {
                'content': text,
            },
        }
        return self.send_message(data)

    def send_image(self, user_id, media_id):
        """
        发送图片消息

        :param str user_id: 发送对象的ID
        :param str media_id: 图片消息的媒体ID
        :return: 发送成功时返回True
        """
        data = {
            'touser': user_id,
            'msgtype': 'image',
            'image': {
                'media_id': media_id,
            },
        }
        return self.send_message(data)

    def send_voice(self, user_id, media_id):
        """
        发送语音消息

        :param str user_id: 发送对象的ID
        :param str media_id: 语音消息的媒体ID
        :return: 发送成功时返回True
        """
        data = {
            'touser': user_id,
            'msgtype': 'voice',
            'voice': {
                'media_id': media_id,
            },
        }
        return self.send_message(data)

    def send_video(self, user_id, media_id, thumb_media_id, title=None, description=None, ):
        """
        发送视频消息

        :param str user_id: 发送对象的ID
        :param str media_id: 视频的媒体ID
        :param str thumb_media_id: 缩略图的媒体ID
        :param str title: 标题(可选)
        :param str description: 视频消息的描述(可选)
        :return: 发送成功时返回True
        """
        video_data = {
            'media_id': media_id,
            'thumb_media_id': thumb_media_id,
        }
        if title:
            video_data['title'] = title
        if description:
            video_data['description'] = description

        data = {
            'touser': user_id,
            'msgtype': 'video',
            'video': video_data,
        }
        return self.send_message(data)

    def send_music(self, user_id, music_url, thumb_media_id,
                   hq_music_url=None, title=None, description=None):
        """
        发送音乐消息

        :param str user_id: 发送对象的ID
        :param str music_url: 音乐链接地址
        :param str thumb_media_id: 缩略图的媒体ID
        :param str hq_music_url: 高品质音乐链接(可选), wifi环境优先使用该链接播放音乐
        :param str title: 标题(可选)
        :param str description: 音乐消息的描述(可选)
        :return: 发送成功时返回True
        """
        if not hq_music_url:
            hq_music_url = music_url
        music_data = {
            'musicurl': music_url,
            'hqmusicurl': hq_music_url,
            'thumb_media_id': thumb_media_id,
        }
        if title:
            music_data['title'] = title
        if description:
            music_data['description'] = description
        data = {
            'touser': user_id,
            'msgtype': 'music',
            'music': music_data,
        }
        return self.send_message(data)

    def send_article(self, user_id, articles=None, media_id=None):
        """
        发送图文消息, 图文消息条数限制在8条以内, 如果图文数超过8, 则将会无响应。

        :param str user_id: 发送对象的ID
        :param list articles: list 对象, 每个元素为一个dict对象, key包含"title", "description", "picurl", "url"
        [
            {
             "title": "Happy Day",
             "description": "Is Really A Happy Day",
             "url": "URL",
             "picurl": "PIC_URL"
            },
            {
             "title": "Happy Day",
             "description": "Is Really A Happy Day",
             "url": "URL",
             "picurl": "PIC_URL"
            },
        ]
        :param str media_id: 图文消息的媒体ID。articles与media_id两种形式二选一
        :return: 发送成功时返回True
        """
        if not articles and not media_id:
            raise Exception('请选择articles或media_id形式之一')

        if articles:
            # 点击跳转到外链
            articles_data = []
            for article in articles:
                articles_data.append({
                    'title': article['title'],
                    'description': article['description'],
                    'url': article['url'],
                    'picurl': article['picurl'],
                })
            data = {
                'touser': user_id,
                'msgtype': 'news',
                'news': {
                    'articles': articles_data,
                },
            }
        else:
            # 点击跳转到图文消息页面
            data = {
                'touser': user_id,
                'msgtype': 'mpnews',
                'mpnews': {
                    'media_id': media_id,
                },
            }
        return self.send_message(data)
