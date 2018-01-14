# coding: utf-8

import django
django.setup()
from web.models import (
    UserInfo,
    Project,
    Comment
)
import poplib
import email
import re
import time
from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr

from settings import EMAILADDRESS, PASSWORD, POP3_SERVER

# 输入邮件地址, 口令和POP3服务器地址:
emailaddress = EMAILADDRESS
# 注意使用开通POP，SMTP等的授权码
password = PASSWORD
pop3_server = POP3_SERVER
# 连接到POP3服务器:
server = poplib.POP3_SSL(pop3_server)
# 可以打开或关闭调试信息:
# server.set_debuglevel(1)
# POP3服务器的欢迎文字:
server.getwelcome()
# 身份认证:
server.user(emailaddress)
server.pass_(password)


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


def get_email_headers(msg):
    # 邮件的From, To, Subject存在于根对象上:
    headers = {}
    for header in ['From', 'To', 'Subject', 'Date', 'x-qq-mid']:
        value = msg.get(header, '')
        if value:
            if header == 'x-qq-mid':
                headers['x-qq-mid'] = value
            if header == 'Date':
                headers['date'] = value
            if header == 'Subject':
                # 需要解码Subject字符串:
                subject = decode_str(value)
                headers['subject'] = subject
            else:
                # 需要解码Email地址:
                hdr, addr = parseaddr(value)
                name = decode_str(hdr)
                value = u'%s <%s>' % (name, addr)
                if header == 'From':
                    from_address = value
                    headers['from'] = from_address
                else:
                    to_address = value
                    headers['to'] = to_address
    content_type = msg.get_content_type()
    print 'head content_type: ', content_type
    return headers


def parsing_email():

    # stat()返回邮件数量和占用空间:
    messagesCount, messagesSize = server.stat()
    # print 'messagesCount:', messagesCount
    # print 'messagesSize:', messagesSize
    # list()返回所有邮件的编号:
    resp, mails, octets = server.list()
    print '------ resp ------'
    print resp  # +OK 46 964346 响应的状态 邮件数量 邮件占用的空间大小
    print '------ mails ------'
    print mails  # 所有邮件的编号及大小的编号list，['1 2211', '2 29908', ...]
    print '------ octets ------'
    print octets

    # 获取最新一封邮件, 注意索引号从1开始:
    length = len(mails)
    for i in range(length):
        resp, lines, octets = server.retr(i + 1)
        # lines存储了邮件的原始文本的每一行,
        # 可以获得整个邮件的原始文本:
        msg_content = '\n'.join(lines)
        # 把邮件内容解析为Message对象：
        msg = Parser().parsestr(msg_content)

        # 但是这个Message对象本身可能是一个MIMEMultipart对象，即包含嵌套的其他MIMEBase对象，
        # 嵌套可能还不止一层。所以我们要递归地打印出Message对象的层次结构：
        print '---------- 解析之后 ----------'
        msg_headers = get_email_headers(msg)
        mail_id = msg_headers['x-qq-mid']
        print 'subject:', msg_headers['subject']
        print 'from_address:', msg_headers['from']
        print 'to_address:', msg_headers['to']
        print 'date:', msg_headers['date']
        print 'x-qq-mid:', mail_id
        j = 0
        content = ''
        user_info = UserInfo.obs.get_queryset().filter(
            email=msg_headers['from'],
        ).first()
        if user_info:
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
                    charset = guess_charset(part)
                    if charset:
                        charset = charset.strip().split(';')[0]
                        data = data.decode(charset)
                    content = data
                    # 解析回复内容，和项目id
                    project_ids = re.findall(r"value=\"(.+?)\"", content)
                    if project_ids:
                        project_id = int(project_ids[0])
                        print '--------------------project-------------------------%s', project_id
                        contents = content.split(u'------')
                        replay_content = contents[0] if contents else ''
                        project = Project.objects.get(pk=project_id)
                        # 回复评论
                        is_comment = Comment.obs.get_queryset().filter(mail_id=mail_id).exists()
                        if not is_comment:
                            Comment.objects.create(
                                user_info=user_info,
                                project=project,
                                content=replay_content,
                                mail_id=mail_id
                            )

    # 关闭连接:
    server.quit()

if __name__ == '__main__':
    parsing_email()
