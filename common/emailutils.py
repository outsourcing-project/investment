# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.utils import parseaddr, formataddr
import smtplib
import poplib
import os
import logging
from email.header import decode_header

from settings import EMAILADDRESS, PASSWORD, POP3_SERVER, SMTP_SERVER


class EmailUtils(object):
    """操作邮件工具类
    """
    def __init__(self, emailaddress, password, pop3_server, smtp_server):
        """初始化类
        """
        self.emailaddress = emailaddress
        self.pop3 = poplib.POP3_SSL(pop3_server)
        self.pop3.user(emailaddress)
        self.pop3.pass_(password)

        self.smtp = smtplib.SMTP_SSL(smtp_server, 465)
        self.smtp.set_debuglevel(1)
        self.smtp.login(emailaddress, password)

    instance = None

    @staticmethod
    def get_instance(emailaddress, password, pop3_server, smtp_server):
        """提供实例的静态方法
        """
        if EmailUtils.instance is None:
            EmailUtils.instance = EmailUtils(emailaddress, password, pop3_server, smtp_server)

        return EmailUtils.instance

    def __format_addr(self, s):
        """邮箱编码处理
        """
        name, addr = parseaddr(s)
        return formataddr((
            Header(name, 'utf-8').encode(),
            addr.encode('utf-8') if isinstance(addr, unicode) else addr))

    def __decode_str(self, s):
        """解码字符串
        """
        value, charset = decode_header(s)[0]
        if charset:
            value = value.decode(charset)
        return value

    def guess_charset(self, msg):
        """获取邮件编码方式
        """
        # 先从msg对象获取编码:
        charset = msg.get_charset()
        if charset is None:
            # 如果获取不到，再从Content-Type字段获取:
            content_type = msg.get('Content-Type', '').lower()
            pos = content_type.find('charset=')
            if pos >= 0:
                charset = content_type[pos + 8:].strip()
        return charset

    def get_email_headers(self, msg):
        """获取邮件header信息
        """
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
                    subject = self.__decode_str(value)
                    headers['subject'] = subject
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = self.__decode_str(hdr)
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

    def send_mail(
            self,
            project_title,
            to_addr,
            context,
            attach_url=None,
            file_name=None):
        """发送邮件
        """
        try:
            msg = MIMEMultipart('alternative')
            msg1 = MIMEText(context, 'html', 'utf-8')

            msg.attach(MIMEText('hello', 'plain', 'utf-8'))
            msg.attach(msg1)
            msg['From'] = self.__format_addr(u'项目评审 <%s>' % from_addr)
            msg['To'] = self.__format_addr(u'<%s>' % to_addr)
            msg['Subject'] = Header(u'%s项目评审' % project_title, 'utf-8').encode()

            # 添加附件就是加上一个MIMEBase，从本地读取一个图片:
            if attach_url:
                from settings import UPLOAD_DIR
                with open(os.path.join(UPLOAD_DIR, attach_url), 'rb') as f:
                    att2 = MIMEText(f.read(), 'base64', 'gb2312')
                    att2["Content-Type"] = 'application/octet-stream'
                    att2["Content-Disposition"] = 'attachment; filename="' + file_name.encode('gbk') + '"'
                    print att2["Content-Disposition"]
                    msg.attach(att2)

            self.smtp.sendmail(self.emailaddress, to_addr, msg.as_string())
        except Exception as e:
            logging.error(e)
            logging.error('----------send_mail---------')

    def pop3_quit(self):
        """pop3邮件服务器退出
        """
        self.pop3.quit()

    def smtp_quit(self):
        """smtp邮件服务器退出
        """
        self.smtp.quit()


emailutils = EmailUtils.get_instance(EMAILADDRESS, PASSWORD, POP3_SERVER, SMTP_SERVER)
