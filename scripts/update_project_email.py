# coding: utf-8

import django
django.setup()
from web.models import (
    UserInfo,
    InvestmentTeam,
    Project,
)

from h5.views.project_view import create_send_email_html
from common.email_utils import send_mail
import datetime

def update_project_email():

    # 检查超过72小时的项目
    expire_time = datetime.datetime.now() - datetime.timedelta(days=2)
    project_list = Project.obs.get_queryset().filter(
        is_valid=True,
        created__lt=expire_time
    ).exclude(investment_team_email='')

    for p in project_list:
        # 成功则发送邮件
        project_title = p.name
        # 获取专家团邮箱
        investment_team_list = InvestmentTeam.obs.get_queryset().filter(
            is_valid=True
        )
        emails = [it.email for it in investment_team_list]
        if emails:
            to_addr = emails
            context = create_send_email_html(p.id)
            attach_url = p.attachment.file if p.attachment else ''
            file_name = p.attachment.title if p.attachment else ''
            send_mail(project_title, to_addr, context, attach_url, file_name)
            p.investment_team_email = ','.join(to_addr)
            p.save()

if __name__ == '__main__':
    update_project_email()
