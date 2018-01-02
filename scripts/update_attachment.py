# coding: utf-8

import django
django.setup()
from web.models import (
    UserInfo,
    Attachment,
)
from imagestore import get_extension
from email import parser
import os
import sys
import locale
import poplib
import email
import logging
import time
# 确定运行环境的encoding
__g_codeset = sys.getdefaultencoding()
if "ascii" == __g_codeset:
    __g_codeset = locale.getdefaultlocale()[1]


def mbs_to_utf8(s):
    return s.decode(__g_codeset).encode("utf-8")

host = 'pop.qq.com'
username = '2274841039@qq.com'
password = 'gdbxsbkajevneaeb'
auth_code = 'gdbxsbkajevneaeb'

pop_conn = poplib.POP3_SSL(host)
pop_conn.user(username)
pop_conn.pass_(password)


def download_attachment():

    userinfo_list = UserInfo.obs.get_queryset().filter(
        is_valid=True,
    )
    userinfo_emails = [u.email for u in userinfo_list]
    messages = [pop_conn.retr(i)
                for i in range(1, len(pop_conn.list()[1]) + 1)]
    messages = ["\n".join(mssg[1]) for mssg in messages]
    messages = [parser.Parser().parsestr(mssg) for mssg in messages]
    i = 0
    for index in range(0, len(messages)):
        message = messages[index]
        i = i + 1
        subject = message.get('subject')
        h = email.Header.Header(subject)
        dh = email.Header.decode_header(h)
        subject = unicode(dh[0][0], dh[0][1]).encode('utf8')
        mailName = "mail%d.%s" % (i, subject)
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
                    data = part.get_payload(decode=True)
                    h = email.Header.Header(fileName)
                    dh = email.Header.decode_header(h)
                    fname = dh[0][0]
                    encodeStr = dh[0][1]
                    if encodeStr is not None:
                        fname = fname.decode(encodeStr, mycode)

                    from settings import UPLOAD_DIR
                    ts = int(time.time())
                    ext = get_extension(fname)
                    key = 'investment_{}.{}'.format(ts, ext)
                    fEx = open(
                        os.path.join(
                            UPLOAD_DIR,
                            key),
                        'wb')
                    fEx.write(data)
                    fEx.close()
                    # 存入附件表中
                    Attachment.objects.create(
                        user_info=userinfo,
                        file=key,
                        title=fname,
                    )
                elif contentType == 'text/plain':  # or contentType == 'text/html':
                    # 保存正文
                    data = part.get_payload(decode=True)
                    content = str(data)
                    if mycode == 'gb2312':
                        content = mbs_to_utf8(content)
                    # end if
                    nPos = content.find('降息')
                    print("nPos is %d" % (nPos))
                    print >> data

        # f.close()

    pop_conn.quit()


if __name__ == '__main__':
    download_attachment()
