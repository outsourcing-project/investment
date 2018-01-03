# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.mime.application import MIMEApplication
from email.utils import parseaddr, formataddr
import smtplib
import os
import logging


def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((
        Header(name, 'utf-8').encode(),
        addr.encode('utf-8') if isinstance(addr, unicode) else addr))


smtp_server = 'smtp.qq.com'
from_addr = '2274841039@qq.com'
password = 'atyxurlcmkaxdiea'
to_addr = '631378725@qq.com'


def send_mail(project_title, to_addr, context, attach_url=None, file_name=None):

    try:
        msg = MIMEMultipart('alternative')

        msg1 = MIMEText(context, 'html', 'utf-8')

        msg.attach(MIMEText('hello', 'plain', 'utf-8'))
        msg.attach(msg1)
        msg['From'] = _format_addr(u'项目评审 <%s>' % from_addr)
        msg['To'] = _format_addr(u'<%s>' % to_addr)
        msg['Subject'] = Header(u'%s项目评审' % project_title, 'utf-8').encode()

        # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
        if attach_url:
            from settings import UPLOAD_DIR
            print os.path.join(UPLOAD_DIR, attach_url)
            part = MIMEApplication(open(os.path.join(UPLOAD_DIR, attach_url), 'rb').read())
            part.add_header('Content-Type', 'application/octet-stream')
            part.add_header(
                'Content-Disposition',
                'attachment',
                filename=file_name)
            part.add_header('Content-ID', '<0>')
            part.add_header('X-Attachment-Id', '0')
            # 把附件的内容读进来:
            # encoders.encode_base64(part)
            msg.attach(part)


            with open(os.path.join(UPLOAD_DIR, attach_url), 'wb') as f:
                # 设置附件的MIME和文件名，这里是png类型:
                mime = MIMEBase('image', 'pdf', filename=file_name)
                # 加上必要的头信息:
                mime.add_header('Content-Type', 'application/octet-stream')
                mime.add_header(
                    'Content-Disposition',
                    'attachment',
                    filename=file_name)
                mime.add_header('Content-ID', '<0>')
                mime.add_header('X-Attachment-Id', '0')
                # 把附件的内容读进来:
                mime.set_payload(f.read())
                # 用Base64编码:
                encoders.encode_base64(mime)
                # 添加到MIMEMultipart:
                msg.attach(mime)

        server = smtplib.SMTP_SSL(smtp_server, 465)
        # server.set_debuglevel(1)
        server.login(from_addr, password)
        server.sendmail(from_addr, to_addr, msg.as_string())
        server.quit()
    except Exception as e:
        logging.error(e)
        logging.error('----------send_mail---------')


if __name__ == "__main__":
    pass
    # project_title = 'asdfasdfasdfasdfasdf'
    # context = '<html><body><h1>Hello</h1>' + '<p>send by <a href="http://www.python.org">Python</a>...</p>' + '</body></html>'
    # attach_url = ''
    # file_name = ''
    # send_mail(project_title, to_addr, context, attach_url, file_name)
