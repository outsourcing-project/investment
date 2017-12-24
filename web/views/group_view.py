# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import Group, User

from guardian.shortcuts import assign_perm, get_perms, remove_perm

from web.models import ACL
from web.decorators import web_permission_required


def group_list(request):
    context = {}
    context['module'] = 'group'

    groups = Group.objects.all()
    acls = ACL.objects.all()
    context['groups'] = groups
    context['acls'] = acls

    return render(request, 'web/group/index.html', context)


# @web_permission_required(codename='add_module', module='group')
def group_add(request):
    context = {}

    acls = ACL.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name', '')

        while True:
            if not name:
                context['error'] = '用户组名称不能为空'
                break

            group = Group()
            group.name = name
            group.save()
            for acl in acls:
                codenames = request.POST.getlist(acl.module, [])
                for codename in codenames:
                    assign_perm(codename, group, acl)

            return HttpResponseRedirect(reverse('web:group_list'))

    context['acls'] = acls
    context['module'] = 'group'

    return render(request, 'web/group/add.html', context)


def group_edit(request, group_id):
    context = {}
    context['module'] = 'group'

    group = get_object_or_404(Group, id=group_id)
    acls = ACL.objects.all()
    context['acls'] = acls
    context['group'] = group

    if request.method == 'POST':
        name = request.POST.get('name', '')

        while True:
            if not name:
                context['error'] = '用户组名称不能为空'
                break

            group.name = name
            group.save()
            for acl in acls:
                old_perms = get_perms(group, acl)
                for old_perm in old_perms:
                    remove_perm(old_perm, group, acl)

                codenames = request.POST.getlist(acl.module, [])
                for codename in codenames:
                    assign_perm(codename, group, acl)

            return HttpResponseRedirect(reverse('web:group_list'))

    return render(request, 'web/group/add.html', context)


def group_delete(request, group_id):
    group = get_object_or_404(Group, id=group_id)
    if not User.objects.filter(groups=group).exists():
        group.delete()

    return HttpResponseRedirect(reverse('web:group_list'))
