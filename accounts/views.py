# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, HttpResponseRedirect, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, login as auth_login, logout as auth_logout)
from django.contrib.auth.views import password_reset, password_reset_confirm
from django.contrib.auth.decorators import login_required, permission_required
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils.translation import ungettext_lazy as _
from django.contrib.messages import info, error
from .models import ForumProfile
from utils.bbs_utils import alphanumeric
from utils.email import send_approve_mail, send_verification_mail, next_url


def index(request):
    return render(request, 'bbs/index.html')


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
        # 注册成功后重定向到首页
        new_user = User.objects.create_user(username, email ,password)
        if not new_user.is_active:
            if settings.ACCOUNT_APPROVAL_REQUIRED:
                send_approve_mail(request, new_user)
                info(request, "感谢注册完毕！当你的账户激活之后你将收到一封邮件.")
            else:
                send_verification_mail(request, new_user, "注册验证")
                info(request, "验证链接邮件已经发送")
            return redirect(next_url(request) or "/")
        else:
            info(request, "已经成功注册")
            return HttpResponseRedirect(reverse('accounts'))


def signup_verify(request, uidb36=None, token=None):
    user = authenticate(uidb36=uidb36, token=token, is_active=False)
    # user = authenticate(username=username, password=password)
    if user is not None:
        user.is_active =True
        p = ForumProfile()
        p.user = user
        p.save()
        auth_login(request, user)
        info(request, "Successfully signed up")
    else:
        error(request, "The link you clicked is no longer valid.")
        return redirect("/")


def user_login(request):
    if request.method == 'GET':
        return render(request, 'account/login.html',)
    elif request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)

        if not User.objects.filter(username=username).exists():
            return render(request, 'account/login.html', {'don_exist': '请求用户不存在'})

        elif not user:
            return render(request, 'account/login.html', {'user_pwd_not': '用户未能通过验证'})

        auth_login(request, user)
        return HttpResponseRedirect('/')


def user_info(request, user_id):
    user = User.objects.get(user=user_id)
    if not ForumProfile.objects.filter(user_id=user.id).exists():
        pf = ForumProfile()
        pf.username = user
        pf.save()
    ctx = {'user': user, }
    return render(request,'account/user_info.html', ctx)


def user_logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('index'))


def reset_pwd(request):
    return password_reset(request, template_name='accounts/reset_password.html',
                          email_template_name='accounts/reset_password_email.html',
                          subject_template_name='accounts/reset_password_subject.txt',
                          post_reset_redirect=reverse('sign_in')
                          )


def reset_confirm(request, uidb64=None, token=None):
    return password_reset_confirm(
        request, template_name='accounts/reset_password_confirm.html',
        uidb64=uidb64, token=token, post_reset_redirect=reverse('sign_in'))
