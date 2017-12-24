# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth import (
    login as django_login,
    logout as django_logout,
    authenticate as django_authenticate,
)

from django.contrib.auth.models import User, Group
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from web.decorators import web_login_required


def account_login(request):
    context = {}

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = django_authenticate(username=username, password=password)
        if user is not None and user.is_active and user.is_staff:
            django_login(request, user)
            next_url = request.GET.get('next', reverse('web:index'))

            return HttpResponseRedirect(next_url)
        else:
            context['error'] = '帐号/密码不正确'

    return render(request, 'web/login.html', context)


@web_login_required
def account_logout(request):
    django_logout(request)
    return HttpResponseRedirect(reverse('web:login'))


@web_login_required
def account_list(request):
    context = {}
    context['module'] = 'account'

    accounts = User.objects.filter(
        Q(is_staff=True),
        Q(is_superuser=False),
    )
    # accounts = User.objects.all()

    context['accounts'] = accounts

    return render(request, 'web/account/index.html', context)


@web_login_required
def account_add(request):
    context = {}
    context['module'] = 'account'
    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        group_id_list = request.POST.getlist('group_id', '')
        group_list = Group.objects.filter(id__in=group_id_list)

        while True:
            if not username:
                context['error'] = '用户名不能为空'
                break

            if not firstname:
                context['error'] = '姓名不能为空'
                break

            if password != password2:
                context['error'] = '两次密码不一致'
                break

            if not password:
                context['error'] = '密码不能为空'
                break

            try:
                account = User.objects.create_user(
                    username=username,
                    password=password
                )
            except Exception as e:
                context['error'] = '该用户名已经存在, 请换一个用户名试试'
                break

            account.first_name = firstname
            account.is_staff = True
            account.is_active = True
            account.groups = list(group_list)
            account.save()
            return HttpResponseRedirect(reverse('web:account_list'))

    groups = Group.objects.all()
    context['groups'] = groups

    return render(request, 'web/account/add.html', context)


@web_login_required
def account_edit(request, account_id):
    context = {}
    context['module'] = 'account'
    account = get_object_or_404(User, pk=account_id)

    if request.method == 'POST':
        username = request.POST.get('username')
        firstname = request.POST.get('firstname')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        group_id_list = request.POST.getlist('group_id', '')
        group_list = Group.objects.filter(id__in=group_id_list)
        while True:
            if not username:
                context['error'] = '用户名不能为空'
                break

            if not firstname:
                context['error'] = '姓名不能为空'
                break

            if password != password2:
                context['error'] = '两次密码不一致'
                break

            try:
                account.username = username
                account.first_name = firstname
                if password:
                    account.password = make_password(password)
                account.groups = list(group_list)
                account.save()

            except Exception as e:
                context['error'] = '该用户名已经存在, 请换一个用户名试试'
                break

            return HttpResponseRedirect(reverse('web:account_list'))

    context['account'] = account
    groups = Group.objects.all()
    context['groups'] = groups

    return render(request, 'web/account/add.html', context)


@web_login_required
def account_offline(request, account_id):
    account = get_object_or_404(User, pk=account_id)
    if account.is_active:
        account.is_active = False
    else:
        account.is_active = True

    account.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@web_login_required
def account_delete(request, account_id):
    account = get_object_or_404(User, pk=account_id)
    account.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
