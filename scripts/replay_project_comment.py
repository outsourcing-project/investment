# coding: utf-8

import django
django.setup()
from web.models import (
    UserInfo,
    Project,
    Comment
)
import email
import re
from email.parser import Parser
from common.emailutils import emailutils

def parsing_email():
    pop3 = emailutils.pop3
    # stat()返回邮件数量和占用空间:
    messagesCount, messagesSize = pop3.stat()
    # print 'messagesCount:', messagesCount
    # print 'messagesSize:', messagesSize
    # list()返回所有邮件的编号:
    resp, mails, octets = pop3.list()
    print '------ resp ------'
    print resp  # +OK 46 964346 响应的状态 邮件数量 邮件占用的空间大小
    print '------ mails ------'
    print mails  # 所有邮件的编号及大小的编号list，['1 2211', '2 29908', ...]
    print '------ octets ------'
    print octets

    # 获取最新一封邮件, 注意索引号从1开始:
    length = len(mails)
    for i in range(length):
        resp, lines, octets = pop3.retr(i + 1)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = '\n'.join(lines)
        # 把邮件内容解析为Message对象：
        msg = Parser().parsestr(msg_content)

        # 但是这个Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，
        # 嵌套可能还不止一层。所以我们要递归地打印出Message对象的层次结构：
        print '---------- 解析之后 ----------'
        msg_headers = emailutils.get_email_headers(msg)
        mail_id = msg_headers['x-qq-mid']
        print 'subject:', msg_headers['subject']
        print 'from_address:', msg_headers['from']
        print 'to_address:', msg_headers['to']
        print 'date:', msg_headers['date']
        print 'x-qq-mid:', mail_id
        j = 0
        content = ''
        for part in msg.walk():
            j = j + 1
            file_name = part.get_filename()
            contentType = part.get_content_type()
            # 保存附件
            project_id = 0
            if contentType == 'text/plain':
                pass
            elif contentType == 'text/html':
                # 保存正文
                data = part.get_payload(decode=True)
                charset = emailutils.guess_charset(part)
                if charset:
                    charset = charset.strip().split(';')[0]
                    data = data.decode(charset)
                content = data
                # 解析回复内容，和项目id
                project_ids = re.findall(r"value=\"(.+?)\"", content)
                if project_ids:
                    project_id = int(project_ids[0])
                    print '--------------------project--------------------%s', project_id
                    contents = content.split(u'------')
                    replay_content = contents[0] if contents else ''
                    project = Project.objects.filter(pk=project_id).first()
                    # 回复评论
                    is_comment = Comment.obs.get_queryset().filter(mail_id=mail_id).exists()
                    if not is_comment and project:
                        Comment.objects.create(
                            email=msg_headers['from'],
                            project=project,
                            content=replay_content,
                            mail_id=mail_id
                        )
    # 关闭连接
    # emailutils.smtp_quit()

if __name__ == '__main__':
    parsing_email()
