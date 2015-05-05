# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from django import template
from django.db import models
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as tz_now
from django.utils.safestring import mark_safe
import re

register = template.Library()
media_file_regex = re.compile(r"<object .+? </object>|" r"<(img|embed) [^>]+>")


@register.filter()
def get_first_media(content):
    m = media_file_regex.search(content)
    media_tag = ""
    if m:
        media_tag = m.group()
    return mark_safe(media_tag)


@register.filter()
def days_since(value):
    today = tz_now().date()
    if isinstance(value, datetime.datetime):
        value = value.date()
    diff = today - value
    if diff.days > 1:
        return _('%s days ago') % diff.days
    elif diff.days == 1:
        return _('yesterday')
    elif diff.days == 0:
        return _('today')
    else:
        return value.strftime("%B %d, %Y")


@register.filter()
def humanize_url(url, letter_count):
    letter_count = int(letter_count)
    re_start = re.compile(r"^https?://")
    re_end = re.compile(r"/$")
    url = re_end.sub("", re_start.sub("", url))
    if len(url) > letter_count:
        url = u"%s..." % url[:letter_count - 1]
        return url


@register.tag
def try_to_include(parser, token):
    try:
        tag_name, template_name = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires a single argument" % token.contents.split()[0]
    return IncludeNode(template_name)


class IncludeNode(template.Node):
    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        try:
            template_name = template.resolve_variable(self.template_name, context)
            included_template = get_template(template_name).render(context)
        except template.TemplateDoesNotExist:
            included_template = ""
        return included_template


@register.tag
def get_objects(parser, token):
    """
    获取指定app名称和模型名称的一组查询集合
    用法：{% get_objects [<manager>.<method> from <app_name>.<model_name>] [limit <amount>] as <var_name> %}
    例子：{% get_objects latest_published from people.Person limit 3 as people %}
    """
    amount = None
    try:
        tag_name, manager_method, str_from, appmodel, str_limit, amount, str_as, var_name = token.split_contents()
    except ValueError:
        try:
            tag_name, manager_method, str_from, appmodel, str_as, var_name = token.split_contents()
        except ValueError:
            raise template.TemplateSyntaxError, "get_objects tag requires a following syntax: {% get_objects " \
                                                "[<manager>.]<method> from <app_name>.<model_name> [limit <amount>] as" \
                                                " <var_name> %}"
    try:
        app_name, model_name = appmodel.split(".")
    except ValueError:
        raise template.TemplateSyntaxError, "get_objects tag requires application name and model name separated by a dot"
    model = models.get_model(app_name, model_name)
    return ObjectsNode(model, manager_method, amount, var_name)


class ObjectsNode(template.Node):
    def __init__(self, model, manager_method, amount, var_name):
        self.model = model
        self.manager_method = manager_method
        self.amount = amount
        self.var_name = var_name

    def render(self, context):
        if "." in self.manager_method:
            manager, method = self.manager_method.split(".")
        else:
            manager = "_default_manager"
            method = self.manager_method

        qs = getattr(
            getattr(self.model, manager),
            method,
            self.model._default_manager.none, )()
        if self.amount:
            amount = template.resolve_variable(self.amount, context)
            context[self.var_name] = qs[:amount]
        else:
            context[self.var_name] = qs
        return ""