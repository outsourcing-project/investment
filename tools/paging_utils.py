# coding: utf-8

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def paging_objs(object_list, per_page, page):

    paginator = Paginator(object_list, per_page)
    try:
        objs = paginator.page(page)
    except PageNotAnInteger:
        objs = []
    except EmptyPage:
        objs = []

    return objs
