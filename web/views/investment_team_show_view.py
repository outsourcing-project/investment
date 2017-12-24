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
    InvestmentTeamShow,
)

from django.db.models import Q
from django.contrib.auth.hashers import make_password
from web.decorators import web_login_required
from utils.file_utils import (
    save_file,
)


@web_login_required
def list(request):
    context = {}
    context['module'] = 'investment_show'
    investment_team_show_list = InvestmentTeamShow.obs.get_queryset().order_by('-order_no')
    context['clients'] = investment_team_show_list

    return render(request, 'web/investment_team_show/index.html', context)


@web_login_required
def add(request):
    context = {}
    context['module'] = 'investment_show'
    if request.method == 'POST':
        title = request.POST.get('title')
        img = request.FILES.get('img', '')

        investment_team_show = InvestmentTeamShow()

        if img:
            img = save_file(img, 'investment_show')
            investment_team_show.img = img

        investment_team_show.title = title
        investment_team_show.save()
        investment_team_show.order_no = investment_team_show.id
        investment_team_show.save()
        return HttpResponseRedirect(reverse('web:investment_team_show_list'))

    return render(request, 'web/investment_team_show/add.html', context)


@web_login_required
def edit(request, investment_team_show_id):
    context = {}
    context['module'] = 'investment_show'
    investment_team_show = get_object_or_404(InvestmentTeamShow, pk=investment_team_show_id)

    if request.method == 'POST':
        title = request.POST.get('title')
        img = request.FILES.get('img', '')

        if img:
            img = save_file(img, 'investment_show')
            investment_team_show.img = img

        investment_team_show.title = title
        investment_team_show.save()
        return HttpResponseRedirect(reverse('web:investment_team_show_list'))

    context['client'] = investment_team_show

    return render(request, 'web/investment_team_show/add.html', context)


@web_login_required
def down(request, investment_team_show_id):
    investment_team_show = get_object_or_404(InvestmentTeamShow, id=investment_team_show_id)

    before_investment_team_shows = InvestmentTeamShow.objects.filter(
        Q(order_no__lt=investment_team_show.order_no) & ~Q(is_del=True)
    ).order_by('-order_no')

    if before_investment_team_shows:
        before_investment_team_show = before_investment_team_shows[0]
        old_order_no = investment_team_show.order_no
        investment_team_show.order_no = before_investment_team_show.order_no
        investment_team_show.save()
        before_investment_team_show.order_no = old_order_no
        before_investment_team_show.save()

    return HttpResponseRedirect(request.session.get('back_url', reverse('web:investment_team_show_list')))


@web_login_required
def up(request, investment_team_show_id):
    investment_team_show = get_object_or_404(InvestmentTeamShow, id=investment_team_show_id)

    after_investment_team_shows = InvestmentTeamShow.objects.filter(
        Q(order_no__gt=investment_team_show.order_no) & ~Q(is_del=True)
    ).order_by('order_no')

    if after_investment_team_shows:
        after_investment_team_show = after_investment_team_shows[0]
        old_order_no = investment_team_show.order_no
        investment_team_show.order_no = after_investment_team_show.order_no
        investment_team_show.save()
        after_investment_team_show.order_no = old_order_no
        after_investment_team_show.save()

    return HttpResponseRedirect(request.session.get('back_url', reverse('web:investment_team_show_list')))


@web_login_required
def delete(request, investment_team_show_id):
    investment_team_show = get_object_or_404(InvestmentTeamShow, pk=investment_team_show_id)
    investment_team_show.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
