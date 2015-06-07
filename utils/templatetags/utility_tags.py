# -*- coding: utf-8 -*-
from datetime import datetime

from django import template
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as tz_now
from django.utils.safestring import mark_safe
register = template.Library()
import re

def days_since(value):
    """
    返回天和值之间的天数
    """
    today = tz_now().date()
    if isinstance(value, datetime.datetime):            # 判断所输入的值是否为datetime对象
        value = value.date()
    diff = today - value
    if diff.days > 1:
        return _("{} days ago".format(diff.days))


media_file_regex = re.compile(r"<img .+?/>")