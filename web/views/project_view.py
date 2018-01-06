# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from web.models import (
    Project,
    Comment,
)

from tools.paging_utils import (
    paging_objs,
)
from tools.qiniu_utils import (
    get_extension,
    handle_uploaded_file,
)

import time


@staff_member_required(login_url='/admin/login')
def list(request):

    context = {}
    context['module'] = 'project'
    objs = Project.obs.get_queryset().order_by('-created')

    search_name = request.GET.get('search_name', None)
    if search_name:
        context['search_name'] = search_name
        objs = objs.filter(name__icontains=search_name)

    page = request.GET.get('page', 1)
    projects = paging_objs(object_list=objs, per_page=10, page=page)

    context['page'] = page
    context['clients'] = projects

    return render(request, 'web/project/index.html', context)


@staff_member_required(login_url='/admin/login')
def delete(request, project_id):
    page = request.GET.get('page', 1)
    search_name = request.GET.get('search_name', '')
    project = Project.objects.get(id=project_id)
    project.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def top(request, project_id):
    page = request.GET.get('page', 1)
    search_name = request.GET.get('search_name', '')
    project = Project.objects.get(id=project_id)
    project.set_top()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def un_top(request, project_id):
    page = request.GET.get('page', 1)
    search_name = request.GET.get('search_name', '')
    project = Project.objects.get(id=project_id)
    project.un_top()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def down_attach(request, project_id):
    page = request.GET.get('page', 1)
    search_name = request.GET.get('search_name', '')
    project = Project.objects.get(id=project_id)
    project.activate()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def comment_list(request):
    context = {}
    context['module'] = 'comment'
    objs = Comment.obs.get_queryset().order_by('-created')
    search_project_name = request.GET.get('search_project_name', '')
    search_content = request.GET.get('search_content', '')
    project_id = request.GET.get('project_id', 0)
    if search_project_name:
        context['search_project_name'] = search_project_name
        objs = objs.filter(project__name__icontains=search_project_name)

    if search_content:
        context['search_content'] = search_content
        objs = objs.filter(content__icontains=search_content)

    if project_id:
        objs = objs.filter(project__pk=project_id)

    page = request.GET.get('page', 1)
    projects = paging_objs(object_list=objs, per_page=10, page=page)

    context['page'] = page
    context['clients'] = projects

    return render(request, 'web/project/comment/index.html', context)


@staff_member_required(login_url='/admin/login')
def comment_delete(request, comment_id):
    page = request.GET.get('page', 1)
    search_name = request.GET.get('search_name', '')
    comment = Comment.objects.get(id=comment_id)
    comment.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

