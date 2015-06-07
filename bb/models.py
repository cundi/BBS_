# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from uuslug import uuslug
import markdown

from utils.bbs_utils import get_delta_time
from DjangoUeditor.models import UEditorField


# 论坛目录结构：
# 论坛首页展现所有板块和分区板块，每个板块下分为若干话题，
# 用户发表话题之下是用户自己和其他用户的回帖
# 板块(Category) <---> 分区板块(Forum) <---> 帖子(Topic) <---> 回帖(Post) |

STATUS_CHOICES = (
    (1, True),
    (2, False),
)

# 板块
class Category(models.Model):
    title = models.CharField(max_length=40)
    slug = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    # 该板块的所属版主
    category_admin = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='category_admin')
    hidden = models.NullBooleanField(blank=False, null=True, default=False,
                                     help_text=_('如果选中，该板块只对站点注册admin可见')
                                     )
    position = models.IntegerField(_('Position'), blank=True, default=0)

    class Meta():
        ordering = ["title"]
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')

    def __unicode__(self):
        return self.title

    def forum_count(self):
        return self.forums.all().count()

    def get_absolute_url(self):
        return reverse('bb:category', kwargs={'id': self.id})

    @property
    def topics(self):
        return Topic.objects.filter(forum__category=self).select_related()

    @property
    def posts(self):
        return Post.objects.filter(topic__forum_category=self).select_related()

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Category, self).save(*args, **kwargs)


# 分区实现功能：
# 1. 显示该话题下每天的帖子更新数
# 2. 话题总数，所有回帖总数
# 3. 最后一个话题，及其作者、时间
class Forum(models.Model):
    category = models.ForeignKey(Category, verbose_name=_('Category'), blank=True, null=True)
    parent = models.ForeignKey('self', related_name='child_forums', verbose_name=_('Parent forum'),
                               blank=True, null=True)
    title = models.CharField(max_length=200)
    slug = models.CharField(max_length=200)
    avatar = models.ImageField(verbose_name='板块头像', blank=True, null=True)
    description = models.CharField(null=True, blank=True, max_length=300)
    created = models.DateTimeField(verbose_name='creation date and time', auto_now_add=True)
    forum_admin = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, verbose_name='版主', related_name='manager')
    post_count = models.IntegerField(_('回帖计数'), blank=True, default=0)
    topic_count = models.IntegerField(_('帖子计数'), blank=True, default=0)
    hidden = models.BooleanField(_('分区是否隐藏'), blank=False, null=False, default=2, choices=STATUS_CHOICES)

    def __unicode__(self):
        return self.title

    class Meta:
        verbose_name = _("Forum")
        verbose_name_plural = _("Forums")

    # 帖子总数
    def sum_topics(self):
        return sum([t.sum_topics() for t in self.topic_set.all()])

    # 最后即最新被回复的帖子
    @staticmethod
    def last_topic(self):
        try:
            return self.topic_set.order_by('-created', '-id')[0]
        except IndexError:
            return None

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Forum, self).save(*args, **kwargs)


class Tags(models.Model):
    tag = models.CharField(max_length=200)


# 帖子（话题）
class Topic(models.Model):
    # 帖子作者
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # 该话题所属的哪个分区
    forum = models.ForeignKey(Forum, verbose_name='forum of topic')
    title = models.CharField(max_length=100, null=True, blank=True)
    slug = models.CharField(max_length=200)
    content = UEditorField(u'内容', width=600, height=300, toolbars="full", imagePath="images/",
                           filePath="files/", upload_settings={"imageMaxSize": 1204000}, settings={}, command=None,
                           blank=True
                           )
    # 话题查看计数
    view_count = models.IntegerField(default=0)
    # 话题回复
    reply_count = models.IntegerField(default=0)
    last_replied_time = models.DateTimeField(blank=True, null=True)
    time_created = models.DateTimeField(auto_now_add=True)
    # 帖子最后编辑时间
    updated = models.DateTimeField(auto_now_add=True)
    # 对帖子的锁定
    is_active = models.BooleanField(choices=STATUS_CHOICES, default=1)
    is_read = models.BooleanField(choices=STATUS_CHOICES, default=2)
    # 帖子是否置顶
    is_top = models.BooleanField(choices=STATUS_CHOICES, default=False)
    order = models.IntegerField(default=10)
    # 控制贴子的删除与否
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=2)
    # 帖子订阅者
    subscribers = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='subscriptions', verbose_name='订阅人', blank=True)

    class Meta():
        ordering = ['order', '-time_created']

    def __unicode__(self):
        return unicode(self.author) + " - " + self.title

    # 在帖子列表中显示用户的头像
    def get_display_datetime(self):
        return get_delta_time(self.created)

    def get_reply_count(self):
        return Topic.objects.filter(reply=self, is_active=True).count()

    # 帖子最新回帖
    def last_post(self):
        if self.post_set.count():
            return self.post_set.order_by('time_created')

    # 标记用户是否读取过该帖子
    def topic_set_is_read(self, user):
        if self.user == user:
            Topic.objects.filter(replys=self).update(is_read=True)

    def get_absolute_url(self):
        return "/topic/{}".format(self.title)

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Topic, self).save(*args, **kwargs)


# 对话题（帖子）的回复，即回帖
class Post(models.Model):
    # 回帖作者
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    # 被回复的那个帖子
    topic = models.ForeignKey(Topic)
    slug = models.CharField(max_length=200)
    content = UEditorField(width=600, height=300, toolbars="full", imagePath="images/",
                           filePath="files/", upload_settings={"imageMaxSize": 1204000}, settings={}, command=None,
                           blank=True
                           )
    time_created = models.DateTimeField(auto_now_add=True, db_index=True)
    updated = models.DateTimeField(
        verbose_name=u'回帖最后编辑时间', blank=True, null=True)
    user_ip = models.GenericIPAddressField(verbose_name='发帖人IP地址', null=True, default='0.0.0.0')
    # 决定回帖是否被删除
    deleted = models.BooleanField(choices=STATUS_CHOICES, default=2)

    class Meta():
        ordering = ['time_created']

    def __unicode__(self):
        return str(self.id) + self.topic.title

    def save(self, *args, **kwargs):
        self.slug = uuslug(self.title, instance=self)
        super(Post, self).save(*args, **kwargs)


class Notification(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_notifications')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_nofitications')
    topic = models.ForeignKey(Topic, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    read = models.BooleanField(default=True)
    time_created = models.DateTimeField(auto_now_add=True)


class Mention(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_mentions')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_mentions')
    post = models.ForeignKey(Post, blank=True, null=True)
    topic = models.ForeignKey(Topic, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    read = models.BooleanField(default=False)
    time_created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-time_created']


class Appendix(models.Model):
    topic = models.ForeignKey(Topic)
    time_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    content_rendered = models.TextField()

    def __unicode__(self):
        return self.topic.title + '-Appendix'

    def save(self, *args, **kwargs):
        if not self.content:
            self.content = ''
        self.content_rendered = markdown.markdown(self.content, ['codehilite'],
                                                  safe_mode='escape')
        super(Appendix, self).save(*args, **kwargs)
