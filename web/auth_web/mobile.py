# coding: utf-8

from django.contrib.auth.models import User
from web.models import UserInfo


class MobileBackend(object):

    def authenticate(self, mobile=None, password=None):
        try:
            userinfo = UserInfo.objects.get(mobile=mobile)
            user = userinfo.user
            if user.check_password(password):
                return user
            else:
                return None
        except Userinfo.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
