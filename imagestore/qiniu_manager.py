# coding: utf-8

import os
import logging
import time

from settings import (
    BASE_DIR,
    DOMAIN,
)


def o_url(key):
    print os.path.join(DOMAIN, key)
    print 'sdfasdfasd'
    if key:
        return '{}{}'.format(DOMAIN, key)
    else:
        return ''


def get_extension(filename):
    arr = filename.split('.')
    if not arr:
        return ''

    return arr[-1]


def handle_uploaded_file(f, path):
    from settings import UPLOAD_DIR
    with open(os.path.join(UPLOAD_DIR, path), 'wb') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

