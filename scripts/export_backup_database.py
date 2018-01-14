#-*- coding:utf-8 -*-

import os
import time
import tarfile
import zipfile

from settings import (
    DATABASES
)

db_host = DATABASES['default']['HOST']
db_user = DATABASES['default']['USER']
db_passwd = DATABASES['default']['PASSWORD']
db_name = DATABASES['default']['NAME']
db_charset = "utf8"
db_backup_name = r"/home/bddyq/workspace/data/backup/investment_%s.sql" % (
    time.strftime("%Y%m%d%H%M"))

zip_src = db_backup_name
zip_dest = zip_src + ".zip"


def zip_files():
    f = zipfile.ZipFile(zip_dest, 'w', zipfile.ZIP_DEFLATED)
    f.write(zip_src)
    f.close()
    os.system("rm %s" % zip_src)


if __name__ == "__main__":
    print("begin to dump mysql database pony...")
    print(
        "mysqldump -h'%s' -u'%s' -p'%s' '%s' --default_character-set='%s' > '%s'" %
        (db_host, db_user, db_passwd, db_name, db_charset, db_backup_name))
    os.system(
        "mysqldump -h'%s' -u'%s' -p'%s' '%s' --default_character-set='%s' > '%s'" %
        (db_host, db_user, db_passwd, db_name, db_charset, db_backup_name))
    print("begin zip files...")
    zip_files()
    print("done, pyhon is great!")
