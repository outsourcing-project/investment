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
    InvestmentTeam,
)

from django.db.models import Q
from django.contrib.auth.hashers import make_password
from web.decorators import web_login_required
from utils.paging_utils import (
    paging_objs,
)


@web_login_required
def list(request):
    page = request.GET.get('page', 1)
    search_username = request.GET.get('search_username', '')
    context = {}
    context['module'] = 'investment'
    investment_team_list = InvestmentTeam.obs.get_queryset()
    if search_username:
        context['search_username'] = search_username
        investment_team_list = investment_team_list.filter(username__contains=search_username)

    investment_team_list = paging_objs(object_list=investment_team_list, per_page=10, page=page)

    context['clients'] = investment_team_list

    return render(request, 'web/investment_team/index.html', context)


@web_login_required
def add(request):
    context = {}
    context['module'] = 'investment'
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        investment_team = InvestmentTeam()

        investment_team.username = username
        investment_team.email = email
        investment_team.save()
        return HttpResponseRedirect(reverse('web:investment_team_list'))

    return render(request, 'web/investment_team/add.html', context)


@web_login_required
def edit(request, investment_team_id):
    context = {}
    context['module'] = 'investment'
    investment_team = get_object_or_404(InvestmentTeam, pk=investment_team_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')

        investment_team.username = username
        investment_team.email = email
        investment_team.save()
        return HttpResponseRedirect(reverse('web:investment_team_list'))

    context['client'] = investment_team

    return render(request, 'web/investment_team/add.html', context)


@web_login_required
def offline(request, investment_team_id):
    investment_team = get_object_or_404(InvestmentTeam, pk=investment_team_id)
    investment_team.deactivate()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@web_login_required
def online(request, investment_team_id):
    investment_team = get_object_or_404(InvestmentTeam, pk=investment_team_id)
    investment_team.activate()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@web_login_required
def delete(request, investment_team_id):
    investment_team = get_object_or_404(InvestmentTeam, pk=investment_team_id)
    investment_team.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
