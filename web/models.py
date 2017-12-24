# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.db.models import Count, Sum, Q
from django.contrib.auth.models import User, Permission
from imagestore.qiniu_manager import o_url

import datetime


class BaseModelManager(models.Manager):

    def get_queryset(self):
        return super(
            BaseModelManager,
            self).get_queryset().filter(
            is_del=False)


class BaseModel(models.Model):

    class Meta:
        abstract = True

    is_del = models.BooleanField(default=False, verbose_name='是否删除')
    is_valid = models.BooleanField(default=True, verbose_name='是否可用')
    updated = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
        verbose_name='更新时间')
    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='创建时间')

    objects = models.Manager()  # The default manager.
    obs = BaseModelManager()  # A manager which will ignore the is_del objects.

    def delete(self, *args, **kwargs):
        self.is_del = True
        self.save()

    def kill(self, *args, **kwargs):
        """
        彻底删除对象
        """
        super(BaseModel, self).delete()

    def activate(self, *args, **kwargs):
        """
        更改状态为有效
        """
        self.is_valid = True
        self.save()

    def deactivate(self, *args, **kwargs):
        """
        更改状态为无效
        """
        self.is_valid = False
        self.save()


class UserInfo(BaseModel):

    class Meta(object):
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    USER_LOGIN_CHOICES = (
        (1, '手机用户'),
        (2, '微信用户'),
        (3, '微博用户'),
        (4, 'qq'),
    )

    GENDER_CHOICES = (
        (1, '男'),
        (2, '女')
    )

    user = models.ForeignKey(
        User,
        default=None,
        blank=True,
        null=True,
        verbose_name='用户')
    email = models.CharField(
        max_length=128,
        default='',
        blank=True,
        verbose_name='邮箱')
    user_name = models.CharField(max_length=128, default='', verbose_name='姓名')
    nickname = models.CharField(max_length=128, default='', verbose_name='昵称')
    password = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='密码')
    jwt_token = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='jwt_token')
    openid = models.CharField(
        max_length=255,
        default='',
        verbose_name='openid')
    user_login_type = models.IntegerField(
        choices=USER_LOGIN_CHOICES,
        default=1,
        verbose_name="用户注册类型")
    gender = models.IntegerField(
        choices=GENDER_CHOICES,
        default=1,
        verbose_name='性别')
    age = models.IntegerField(default=0, verbose_name='年龄')
    mobile = models.CharField(
        max_length=16,
        default='',
        blank=True,
        verbose_name='手机')
    avatar = models.CharField(
        max_length=300,
        default='',
        null=True,
        blank=True,
        verbose_name='头像')
    birbath = models.DateField(default=datetime.date.today, verbose_name="生日")
    wx_unionid = models.CharField(
        max_length=300,
        default='',
        blank=True,
        verbose_name="微信id")
    weibo_uid = models.CharField(
        max_length=300,
        default='',
        blank=True,
        verbose_name="微博id")
    qq_uid = models.CharField(
        max_length=300,
        default='',
        blank=True,
        verbose_name="qqid")

    def get_user(self):
        try:
            if not self.user:
                username = self.mobile if self.mobile else self.email
                self.user = User.objects.create_user(
                    username,
                    self.email,
                    self.password
                )
                self.save()
        except Exception as e:
            print e

        return self.user

    def avatar_url(self):
        if 'http' in self.avatar:
            avatar_url = self.avatar
        else:
            avatar_url = o_url(self.avatar)
        return avatar_url

    @property
    def project_count(self):
        project_count = Project.obs.get_queryset().filter(
            user_info=self
        ).count()
        return project_count

    def __unicode__(self):
        return self.nickname


class ACL(BaseModel):

    class Meta(object):

        verbose_name = "访问控制列表"
        verbose_name_plural = "访问控制列表"
        permissions = (
            ('view_module', '查看'),
            ('add_module', '添加'),
            ('edit_module', '编辑'),
            ('delete_module', '删除'),
            ('active_module', '启用禁用'),
            ('move_module', '上移下移'),
        )

    module = models.CharField(max_length=255, default='', verbose_name="模块名称")
    module_cn = models.CharField(
        max_length=255,
        default='',
        verbose_name="模块中文名称")
    permission_ids = models.CharField(
        max_length=255, default='', verbose_name="权限选项")

    def __unicode__(self):
        return self.module

    def permission_options(self):
        ids = self.permission_ids.split('#')
        return Permission.objects.filter(id__in=ids)


class Setting(BaseModel):

    class Meta(object):
        verbose_name = '配置'
        verbose_name_plural = '配置'

    name = models.CharField(max_length=100, default='', verbose_name="字段")
    value = models.CharField(max_length=100, default='', verbose_name="值")
    code = models.CharField(max_length=100, default='', verbose_name="code")


class Project(BaseModel):

    class Meta(object):
        verbose_name = '项目'
        verbose_name_plural = '项目'

    VAILD_CHOICES = (
        (0, '否'),
        (1, '是'),
    )

    user_info = models.ForeignKey(
        UserInfo,
        null=True,
        blank=True,
        verbose_name='用户')
    name = models.CharField(max_length=255, default='', verbose_name="项目名称")
    theme = models.CharField(max_length=255, default='', verbose_name="主控主体")
    total_amount = models.FloatField(
        default=0, blank=True, verbose_name="项目投资总额")
    share_amount = models.FloatField(
        default=0, blank=True, verbose_name="项目投资份额")
    cycle = models.FloatField(default=0, blank=True, verbose_name="投资周期")
    expect_return = models.FloatField(
        default=0, blank=True, verbose_name="预计回报")
    progress = models.CharField(
        max_length=255,
        default='',
        verbose_name="项目进度")
    note = models.TextField(blank=True, default='', verbose_name="备注")
    top = models.IntegerField(
        choices=VAILD_CHOICES,
        default=0,
        verbose_name="是否置顶")
    top_time = models.DateTimeField(
        default=None,
        null=True,
        blank=True,
        verbose_name="置顶时间")
    read_count = models.IntegerField(default=0, verbose_name="浏览量")

    @property
    def comment_count(self):
        return Comment.obs.get_queryset().filter(project=self).count()

    def set_top(self):
        self.top = 1
        self.top_time = datetime.datetime.now()
        self.save()

    def un_top(self):
        self.top = 0
        self.top_time = None
        self.save()


class Attachment(BaseModel):

    class Meta:
        verbose_name = '附件'
        verbose_name_plural = '附件'

    project = models.ForeignKey(
        Project,
        default=None,
        null=True,
        blank=True,
        verbose_name='项目')
    file = models.CharField(max_length=1024, default='', verbose_name='附件')
    title = models.CharField(max_length=1024, default='', verbose_name='附件名称')


class Comment(BaseModel):

    class Meta(object):
        verbose_name = "评论"
        verbose_name_plural = "评论"

    user_info = models.ForeignKey(
        UserInfo,
        null=True,
        blank=True,
        verbose_name='评论用户')
    project = models.ForeignKey(
        Project,
        default=None,
        null=True,
        blank=True,
        verbose_name='项目')
    content = models.TextField(default='', blank=True, verbose_name='内容')


class ExpertTeam(BaseModel):

    class Meta(object):
        verbose_name = "专家团"
        verbose_name_plural = "专家团"

    username = models.CharField(
        max_length=1024,
        default='',
        verbose_name='专家名称')
    email = models.CharField(max_length=1024, default='', verbose_name='email')


class InvestmentTeam(BaseModel):

    class Meta(object):
        verbose_name = "投资团"
        verbose_name_plural = "投资团"

    username = models.CharField(
        max_length=1024,
        default='',
        verbose_name='投资人名称')
    email = models.CharField(max_length=1024, default='', verbose_name='email')


class InvestmentTeamShow(BaseModel):

    class Meta(object):
        verbose_name = "投资团展示"
        verbose_name_plural = "投资团展示"

    order_no = models.IntegerField(default=0, verbose_name="排序号")
    title = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='标题')
    img = models.CharField(max_length=1024, default='', verbose_name='图片')

    @property
    def img_url(self):
        return o_url(self.img)
