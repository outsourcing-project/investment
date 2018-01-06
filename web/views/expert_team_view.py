# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate as django_authenticate,
)

from web.models import (
    ExpertTeam,
)

from django.db.models import Q
from django.contrib.auth.hashers import make_password
from web.decorators import web_login_required

from tools.paging_utils import (
    paging_objs,
)


@web_login_required
def list(request):
    context = {}
    page = request.GET.get('page', 1)
    search_username = request.GET.get('search_username', '')
    context['module'] = 'expert'
    expert_team_list = ExpertTeam.obs.get_queryset()
    if search_username:
        context['search_username'] = search_username
        expert_team_list = expert_team_list.filter(username__contains=search_username)

    expert_team_list = paging_objs(object_list=expert_team_list, per_page=10, page=page)

    context['clients'] = expert_team_list

    return render(request, 'web/expert_team/index.html', context)


@web_login_required
def add(request):
    context = {}
    context['module'] = 'account'
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        expert_team = ExpertTeam()

        expert_team.username = username
        expert_team.email = email
        expert_team.save()
        return HttpResponseRedirect(reverse('web:expert_team_list'))

    return render(request, 'web/expert_team/add.html', context)


@web_login_required
def edit(request, expert_team_id):
    context = {}
    context['module'] = 'expert_team'
    expert_team = get_object_or_404(ExpertTeam, pk=expert_team_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        expert_team.username = username
        expert_team.email = email
        expert_team.save()
        return HttpResponseRedirect(reverse('web:expert_team_list'))

    context['client'] = expert_team

    return render(request, 'web/expert_team/add.html', context)


@web_login_required
def offline(request, expert_team_id):
    expert_team = get_object_or_404(ExpertTeam, pk=expert_team_id)
    expert_team.deactivate()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@web_login_required
def online(request, expert_team_id):
    expert_team = get_object_or_404(ExpertTeam, pk=expert_team_id)
    expert_team.activate()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@web_login_required
def delete(request, expert_team_id):
    expert_team = get_object_or_404(ExpertTeam, pk=expert_team_id)
    expert_team.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
