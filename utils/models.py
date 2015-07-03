# -*- coding: UTF-8 -*-
import urlparse

from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.template.defaultfilters import escape
from django.utils.translation import ugettext_lazy as _
from django.utils.timezone import now as timezone_now
from django.utils.safestring import mark_safe


class UrlMixin(models.Model):
    """
    get_absolute_url()的替代品。模型扩展该mixin便可以执行get_url或者get_url_path。
    """

    class Meta:
        abstract = True

    def get_url(self):
        if hasattr(self.get_url_path, 'dont_recurse'):
            raise NotImplemented
        try:
            path = self.get_url_path()
        except NotImplemented:
            raise
        website_url = getattr(settings, 'DEFAULT_WEBSITE_URL', 'http://127.0.0.1:8000')
        return website_url + path

    get_url.dont_recurse = True

    def get_url_path(self):
        if hasattr(self.get_url, 'dont_recurse'):
            raise NotImplemented
        try:
            url = self.get_url()
        except NotImplemented:
            raise
        bits = urlparse.urlparse(url)
        return urlparse.urlunparse(('', '') + bits[2:])

    get_url_path.dont_recurse = True

    def get_absolute_url(self):
        return self.get_url_path()


class CreationModificationDateMixin(models.Model):
    """
    可以创建和修改日期和时间的抽象基类。
    """
    class Meta:
        abstract = True

    created = models.DateTimeField(
        _("creation date and time"),
        editable=False,
    )

    modified = models.DateTimeField(_("modification date and time"), null=True, editable=False,)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.created = timezone_now()
        else:                              # 为了保证我们一直拥有创建数据，添加下面的条件语句
            if not self.created:
                self.created = timezone_now()
            self.modified = timezone_now()
        super(CreationModificationDateMixin, self).save(*args, **kwargs)

    save.alters_data = True


class MetaTagsMixin(models.Model):
    """
    Abstract base class for meta tags in the <head> section
    <head>元素中由抽象基类所构成的元标签
    """
    meta_keywords = models.CharField(
        _('Keywords'),
        max_length=255,
        blank=True,
        help_text=_("Separate keywords by comma."),
    )
    meta_description = models.CharField(
        _('Description'),
        max_length=255,
        blank=True,
    )
    meta_author = models.CharField(
        _('Author'),
        max_length=255,
        blank=True,
    )
    meta_copyright = models.CharField(
        _('Copyright'),
        max_length=255,
        blank=True,
    )

    class Meta:
        abstract = True

    def get_meta_keywords(self):
        meta_tag = u""
        if self.meta_keywords:
            meta_tag = u"""<meta name="keywords" content="%s" />\n""" % escape(self.meta_keywords)
        return mark_safe(meta_tag)

    def get_meta_description(self):
        meta_tag = u""
        if self.meta_description:
            meta_tag = u"""<meta name="description" content="%s" />\n""" % escape(self.meta_description)
        return mark_safe(meta_tag)

    def get_meta_author(self):
        meta_tag = u""
        if self.meta_author:
            meta_tag = u"""<meta name="author" content="%s" />\n""" % escape(self.meta_author)
        return mark_safe(meta_tag)

    def get_meta_copyright(self):
        meta_tag = u""
        if self.meta_copyright:
            meta_tag = u"""<meta name="copyright" content="%s" />\n""" % escape(self.meta_copyright)
        return mark_safe(meta_tag)

    def get_meta_tags(self):
        return mark_safe(u"".join((
            self.get_meta_keywords(),
            self.get_meta_description(),
            self.get_meta_author(),
            self.get_meta_copyright(),
        )))
