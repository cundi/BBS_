# -*- coding:utf-8 -*-
from django import forms
from django.contrib.auth import authenticate, get_user_model
from django.utils.text import capfirst


class AuthenticationForm(forms.Form):
    """
    认证用户的基类。实现一个接受username/password登录。
    """
    username = forms.CharField(max_length=254)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    error_messages = {
        'invalid_login': '请输入一个正确的 %(username)和密码。注意两个字段的大小写',
        'inactive': '账户未能激活',
    }

    def __init__(self, request=None, *args, **kwargs):
        """
        表单数据通过标准的'data'关键字参数实现
        :param request:
        :param args:
        :param kwargs:
        :return:
        """
        self.request = request
        self.user_cache = None
        super(AuthenticationForm, self).__init__(*args, **kwargs)

        # 设置“username”字段的标签。
        userModel = get_user_model()
        self.username_field = userModel._meta.get_field(userModel.USERNAME_FILED)
        if self.fields['username'].lable is None:
            self.fields['username'].lable = capfirst(self.username_field.verbose_name)

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username and password:
            self.user_cache = authenticate(username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError(
                    self.error_messages['invalid_login'],
                    code='invalid_login',
                    params={'username': self.username_field.verbose_name},
                )
            else:
                self.confirm_login_allowed(self.user_cache)
        return self.cleaned_data

    def confirm_login_allowed(self, user):
        """
        控制给定用户是否可以登录。这是一个策略设定，依赖于终端用户的认证。
        该方法的默认行为是允许激活用户登录，拒绝未激活用户的登录。
        如果给定用户不能够登录，则该方法会抛出“form.ValidationError"异常。
        如果给定用户可以登录，则该方法会返回None。
        :param user:
        :return:
        """
        if not user.is_active:
            raise forms.ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )

    def get_user_id(self):
        if self.user_cache:
            return self.user_cache.id
        return None

    def get_user(self):
        return self.user_cache
