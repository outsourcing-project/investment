# coding: utf-8

import os
import time
import random

from settings import (
    UPLOAD_DIR,
    MEDIA_URL,
)


def save_img(f, prefix):
    return save_file(f, prefix)


def save_file(f, prefix):

    ts = int(time.time())
    rd = random.randint(100000, 999999)
    ext = f.name.split('.')[-1]
    filename = '{}_{}_{}.{}'.format(prefix, ts, rd, ext)

    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, 'wb') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

    url = '{}{}'.format(MEDIA_URL, filename)
    return url


def save_file_with_filename(f, prefix):

    ts = int(time.time())
    rd = random.randint(100000, 999999)
    # ext = f.name.split('.')[-1]
    filename = '{}_{}_{}_{}'.format(prefix, ts, rd, f.name.encode('utf-8'))

    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, 'wb') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

    url = os.path.join(MEDIA_URL, filename)
    return url


def file_iterator(file_path, chunk_size=512):
    with open(file_path) as f:
        while True:
            c = f.read(chunk_size)
            if c:
                yield c
            else:
                break
