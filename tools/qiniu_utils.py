# coding: utf-8

import os
from settings import (
    DOMAIN,
)

def my_url(key):
    if key:
        return os.path.join(DOMAIN + '/media/', key)
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