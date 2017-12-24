# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from web.models import ACL


def acl_list(request):
    context = {}
    context['module'] = 'acl'
    search_id = request.GET.get('search_id', None)
    acls = ACL.objects.all()
    if search_id:
        acls = ACL.objects.filter(pk=search_id)
    context['acls'] = acls

    return render(request, 'web/acl/index.html', context)


def acl_add(request):
    context = {}
    context['module'] = 'acl'

    if request.method == 'POST':
        module_cn = request.POST.get('module_cn', '')
        module = request.POST.get('module', '')
        context['module'] = module
        permission_id_list = request.POST.getlist('permission_id', [])
        permission_ids = '#'.join(permission_id_list)

        while True:
            if not module:
                context['error'] = '模块名称不能为空'
                break

            if not module_cn:
                context['error'] = '模块中文名称不能为空'
                break

            acl = ACL()
            acl.module_cn = module_cn
            acl.module = module
            acl.permission_ids = permission_ids
            acl.save()

            return HttpResponseRedirect(reverse('web:acl_list'))

    content_type = ContentType.objects.get_for_model(ACL)
    permissions = Permission.objects.filter(content_type=content_type)
    context['permissions'] = permissions
    print permissions

    return render(request, 'web/acl/add.html', context)


def acl_edit(request, acl_id):
    context = {}
    context['module'] = 'acl'

    acl = get_object_or_404(ACL, id=acl_id)

    if request.method == 'POST':
        module_cn = request.POST.get('module_cn', '')
        module = request.POST.get('module', '')

        permission_id_list = request.POST.getlist('permission_id', [])
        permission_ids = '#'.join(permission_id_list)

        while True:
            if not module:
                context['error'] = '模块名称不能为空'
                break

            if not module_cn:
                context['error'] = '模块中文名称不能为空'
                break

            acl.module_cn = module_cn
            acl.module = module
            acl.permission_ids = permission_ids
            acl.save()

            return HttpResponseRedirect(reverse('web:acl_list'))

    content_type = ContentType.objects.get_for_model(ACL)
    permissions = Permission.objects.filter(content_type=content_type)
    context['acl'] = acl
    context['permissions'] = permissions

    return render(request, 'web/acl/add.html', context)


def acl_delete(request, acl_id):

    page = request.GET.get('page', 1)
    search_id = acl_id
    # acl = get_object_or_404(ACL, id=search_id)
    acl = ACL.objects.filter(id=search_id)
    acl.delete()

    return HttpResponseRedirect(reverse('web:acl_list'))
