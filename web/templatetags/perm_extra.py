# coding: utf-8

from django import template
from django.contrib.auth.models import Permission

from guardian.shortcuts import get_perms

from web.models import ACL

register = template.Library()


@register.filter
def perm_name(perm_codename):
    perm = Permission.objects.filter(codename=perm_codename).first()
    if perm:
        return perm.name
    return ''


@register.filter
def get_acl_perms(user, module):
    try:
        acl = ACL.objects.get(module=module)
        perms = get_perms(user, acl)
        print 'get_acl_perms', perms
        return perms
    except ACL.DoesNotExist:
        return []
