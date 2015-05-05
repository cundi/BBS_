# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django.core.validators import RegexValidator


def get_delta_time(time_in):
    time_delta = datetime.today() - time_in
    day = time_delta.days
    sec = time_delta.seconds
    if day > 0:
        if day / 365 > 0:
            return '%d 年前' % (day / 365)
        else:
            return '%d 天前' % (day % 365)
    else:
        if sec < 60:
            return '1 分钟前'
        elif sec < 3600:
            return '%d 分钟前' % (sec / 60)
        else:
            return '%d 小时 %d 分钟前' % (sec / 3600, (sec % 3600) / 60)

# 对输入用户名的验证
alphanumeric = RegexValidator(r'^[0-9a-zA-Z\_]*$', '只有字母数字和下划线被允许')