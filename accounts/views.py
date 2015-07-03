# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.shortcuts import render, HttpResponseRedirect, redirect
from django.contrib.auth.models import User
from django.contrib.auth import (REDIRECT_FIELD_NAME, authenticate, login as auth_login, logout as auth_logout)
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.sites.shortcuts import get_current_site
from django.core.urlresolvers import reverse
from django.contrib.messages import info, error
from django.utils.http import is_safe_url
from django.shortcuts import resolve_url
from django.template.response import TemplateResponse
from django.views.decorators.cache import never_cache

from django.views.decorators.csrf import csrf_protect

from .models import ForumProfile
from .forms import AuthenticationForm
from utils.bbs_utils import alphanumeric


def index(request):
    return render(request, 'bb/index.html')


@csrf_protect
@never_cache
def user_login(request, template_name='account/login.html',
               redirect_field_name=REDIRECT_FIELD_NAME,
               authentication_form=AuthenticationForm,
               current_app=None, extra_context=None
               ):
    """
    显示登录表单并处理登录行为
    :param request:
    :return:
    """
    redirect_to = request.POST.get(redirect_field_name, request.GET.get(redirect_field_name, ''))

    if request.method == 'POST':
        form = authentication_form(request, data=request.POST)
        if form.is_valid():
            # 保证来自用户的重定向url是安全的。
            if not is_safe_url(url=redirect_to, host=request.get_host()):
                redirect_to = resolve_url(settings.LOGIN_REDIRECT_URL)
            # 完全地安全检查，让用户登录
            return HttpResponseRedirect(redirect_to)
    else:
        form = authentication_form(request)

    current_site = get_current_site(request)

    context = {
        'form': form,
        redirect_field_name: redirect_to,
        'site': current_site,
        'site_name': current_site.name,
    }
    if extra_context is not None:
        context.update(extra_context)

    if current_app is not None:
        request.current_app = current_app

    return TemplateResponse(request, template_name, context)


def user_signup(request):
    error_msg = []
    if request.user.is_authenticated():
        return HttpResponseRedirect('/')
    if request.method == 'GET':
        return render(request, 'account/signup.html')
    elif request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        try:
            alphanumeric(username)
        except:
            # 这里的 messages 传递到signup.html模板中的变量{{ messages }}
            error_msg.append('请检查输入否为数字和字母以及下划线')
            return render(request, 'account/signup.html', {'error': error_msg})

        # 对输入的用户名与数据中的对比
        if User.objects.filter(username=username).exists():
            error_msg.append('用户名已经存在')
            # messages.add_message(request, messages.WARNING, '用户已存在')
            return render(request, 'account/signup.html', {'error': error_msg})

        # 对表单中输入的两次密码进行比对
        if password != password2 or password == '' or password2 == '':
            error_msg.append('两次输入不匹配，或者为空')
            return render(request, 'account/signup.html', {'error': error_msg})
        new_user = User.objects.create_user(username, email, password)


def signup_verify(request, uidb36=None, token=None):
    user = authenticate(uidb36=uidb36, token=token, is_active=False)
    # user = authenticate(username=username, password=password)
    if user is not None:
        user.is_active = True
        p = ForumProfile()
        p.user = user
        p.save()
        auth_login(request, user)
        info(request, "Successfully signed up")
    else:
        error(request, "The link you clicked is no longer valid.")
        return redirect("/")


def user_info(request, user_id):
    user = User.objects.get(user=user_id)
    if not ForumProfile.objects.filter(user_id=user.id).exists():
        pf = ForumProfile()
        pf.username = user
        pf.save()
    ctx = {'user': user, }
    return render(request, 'account/user_info.html', ctx)


def user_logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))


def reset_pwd(request):
    return password_reset(request, template_name='accounts/reset_password.html',
                          email_template_name='accounts/reset_password_email.html',
                          subject_template_name='accounts/reset_password_subject.txt',
                          post_reset_redirect=reverse('sign_in')
                          )


def pwd_reset_done(request, uidb64=None, token=None):
    return password_reset_confirm(
        request, template_name='accounts/reset_password_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('sign_in'))


def pwd_change(request): pass


def pwd_change_done(request):
    pass
