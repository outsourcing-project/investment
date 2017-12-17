# coding: utf-8

from django import template

register = template.Library()


@register.filter
def paging(objs):

    paginator = objs.paginator
    page = objs.number
    per_page = 10
    page_min = None
    page_max = None

    while True:

        if paginator.num_pages < per_page:
            page_min = 1
            page_max = paginator.num_pages
            break

        if page <= per_page / 2:
            page_min = 1
            page_max = per_page
            break

        if page + (per_page / 2) > paginator.num_pages:
            page_max = paginator.num_pages
            page_min = paginator.num_pages - (per_page - 1)
            break

        page_min = page - (per_page / 2)
        page_max = page + (per_page / 2 - 1)
        break

    l = [index for index in range(page_min, page_max + 1)]

    return l


@register.filter
def url_deal(params):

    url = '?'

    if params:
        if 'page' in params:
            params.pop('page')
        key_values = ['='.join(p) for p in params.iteritems()]
        url += '&'.join(key_values)
        url += '&'

    return url
