# -*- coding: utf-8 -*-

from constants import(
    TEMPLATE_SET_INDUSTRY_URL,
    TEMPLATE_GET_INDUSTRY_INFO_URL,
    TEMPLATE_GET_ID_URL,
    TEMPLATE_GET_LIST_URL,
    TEMPLATE_DELETE_URL,
    TEMPLATE_SEND_MESSAGE_URL,
)

from .request_manager import request_manager


class TemplateMessageManager(object):
    """
    微信模板消息管理
    详情请参考 http://mp.weixin.qq.com/wiki/17/304c1885ea66dbedf7dc170d84999a9d.html
    """

    def __init__(self):
        """
        初始化

        :param RequestManager request_manager: RequestManager类的实例
        """
        self.request_manager = request_manager

    def set_industry(self, industry_id1, industry_id2):
        """
        设置所属行业，行业类型与消息模板相关

        :param int industry_id1: 主营行业代码
        :param int industry_id2: 副营行业代码
        :return: 返回json数据包的dict形式
        {
            "errcode": 0,
            "errmsg": "ok",
        }
        """
        industry_id_data = {
            "industry_id1": str(industry_id1),
            "industry_id2": str(industry_id2),
        }
        return self.request_manager.post(
            raw_url=TEMPLATE_SET_INDUSTRY_URL,
            json=industry_id_data,
        )

    def get_industry(self):
        """
        获取设置的行业信息

        :return: 返回json数据包的dict形式
        {
            "primary_industry":{"first_class":"运输与仓储","second_class":"快递"},
            "secondary_industry":{"first_class":"IT科技","second_class":"互联网|电子商务"}
        }
        """
        return self.request_manager.get(
            raw_url=TEMPLATE_GET_INDUSTRY_INFO_URL,
        )

    def get_id(self, template_id_short):
        """
        通过模板编号获得模板实际ID

        :param template_id_short: 模板库中模板的编号，有“TM**”和“OPENTMTM**”等形式
        :return: 返回json数据包的dict形式
        {
            "errcode": 0,
            "errmsg": "ok",
            "template_id": "template_id",
        }
        """
        template_id_short_data = {
            "template_id_short": str(template_id_short),
        }

        return self.request_manager.post(
            raw_url=TEMPLATE_GET_ID_URL,
            json=template_id_short_data,
        )

    def get_list(self):
        """
        获取模板列表

        :return: 返回json数据包的dict形式
        {
            "template_list": [{
                "template_id": "模版ID",
                "title": "模板标题",
                "primary_industry": "模板所属行业的一级行业",
                "deputy_industry": "模版所属行业的二级行业",
                "content": "模板内容",
                "example": "模板示例",
            }],
        }
        :bug-16.7.26: 每调用一次会自动生成一个内容一致，拥有独立ID、内容重复的模板
        """
        return self.request_manager.get(
            raw_url=TEMPLATE_GET_LIST_URL,
        )

    def delete(self, template_id):
        """
        删除模板

        :param str template_id: 模板ID
        :return: 返回json数据包的dict形式
        {
            "errcode": 0,
            "errmsg": "ok",
        }
        """
        template_id_data = {
            "template_id": str(template_id),
        }
        return self.request_manager.post(
            raw_url=TEMPLATE_DELETE_URL,
            json=template_id_data,
        )

    def send_message(self, user_id, template_id, data,
                     url='', topcolor='#FF0000'):
        """
        发送模版消息

        :param str user_id: 消息目标用户ID，如'oYndcxG0WA9nfdyOzPR1VfbcTcws'
        :param str template_id: 模板ID
        :param dict data: 模板消息数据，示例如下：
        {
            "first": {
               "value": "恭喜你购买成功！",
               "color": "#173177"
            },
            "keynote1": {
               "value": "巧克力",
               "color": "#173177"
            },
            "keynote2": {
               "value": "39.8元",
               "color": "#173177"
            },
            "keynote3": {
               "value": "2014年9月16日",
               "color": "#173177"
            },
            "remark":{
               "value": "欢迎再次购买！",
               "color": "#173177"
            },
        }
        :param url: 发送结果反馈地址 (默认为空)
        :param topcolor: 顶部颜色RGB值 (默认 '#FF0000' )
        :return: 返回json数据包的dict形式
        success_res = {
            "errcode": 0,
            "errmsg": "ok",
            "msgid": "message_id",
        }
        """
        message_data = {
            "touser": user_id,
            "template_id": template_id,
            "url": url,
            "topcolor": topcolor,
            "data": data,
        }

        return self.request_manager.post(
            raw_url=TEMPLATE_SEND_MESSAGE_URL,
            json=message_data,
        )

template_message_manager = TemplateMessageManager()
