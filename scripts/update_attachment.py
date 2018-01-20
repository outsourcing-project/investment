# coding: utf-8

import django
django.setup()
from web.models import (
    UserInfo,
    Attachment,
)
from imagestore.qiniu_manager import get_extension
from email import parser
import email
import os
import logging
import time
from common.emailutils import emailutils

def download_attachment():
    pop3 = emailutils.pop3
    userinfo_list = UserInfo.obs.get_queryset().filter(
        is_valid=True,
    )
    userinfo_emails = [u.email for u in userinfo_list]
    messages = [pop3.retr(i)
                for i in range(1, len(pop3.list()[1]) + 1)]
    messages = ["\n".join(mssg[1]) for mssg in messages]
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    i = 0
    for index in range(0, len(messages)):
        message = messages[index]
        i = i + 1
        subject = message.get('subject')
        mail_id = message.get('x-qq-mid')
        h = email.Header.Header(subject)
        dh = email.Header.decode_header(h)
        try:
            subject = unicode(dh[0][0], dh[0][1]).encode('utf8')
        except Exception as e:
            subject = ''
        from_email = email.utils.parseaddr(message.get('from'))[1]
        # f = open('%d.log' % (i), 'w')
        # print >> f, "Date: ", message["Date"]
        # print >> f, "From: ", from_email
        # print >> f, "To: ", email.utils.parseaddr(message.get('to'))[1]
        # print >> f, "Subject: ", subject
        # print >> f, "Data: "
        logging.error('-------------------------------%s', from_email)
        # 发送的邮箱在用户邮箱中则处理
        if from_email in userinfo_emails:
            userinfo = UserInfo.obs.get_queryset().filter(
                is_valid=True,
                email=from_email
            ).first()
            j = 0
            for part in message.walk():
                j = j + 1
                fileName = part.get_filename()
                contentType = part.get_content_type()
                mycode = part.get_content_charset()
                # 保存附件
                if fileName:
                    fileName = fileName.decode('gbk')
                    data = part.get_payload(decode=True)
                    h = email.Header.Header(fileName)
                    dh = email.Header.decode_header(h)
                    for indx, val in enumerate(dh):
                        fname = val[0]
                        encodeStr = val[1]
                        if encodeStr is not None:
                            fname = fname.decode(encodeStr, mycode)

                        # 判断附件是否已经上传过
                        is_upload = Attachment.obs.get_queryset().filter(
                            user_info=userinfo,
                            title=fname,
                            mail_id=mail_id
                        ).exists()
                        if not is_upload:
                            from settings import UPLOAD_DIR
                            ts = int(time.time())
                            ext = get_extension(fname)
                            key = 'investment_{}.{}'.format(ts, ext)
                            try:
                                fEx = open(os.path.join(UPLOAD_DIR, key), 'wb')
                                fEx.write(data)
                                fEx.close()

                                # 存入附件表中
                                attachment = Attachment.objects.create(
                                    user_info=userinfo,
                                    title=fname,
                                )
                                attachment.file = key
                                attachment.save()
                            except Exception as e:
                                print '---------attachment-error----------'

                elif contentType == 'text/plain':  # or contentType == 'text/html':
                    # 保存正文
                    data = part.get_payload(decode=True)
                    charset = emailutils.guess_charset(part)
                    if charset:
                        charset = charset.strip().split(';')[0]
                        data = data.decode(charset)

        # f.close()

    # 关闭连接
    emailutils.smtp_quit()


if __name__ == '__main__':
    download_attachment()
