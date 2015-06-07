# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import get_random_string
from bb.models import Topic



class ForumProfile(AbstractBaseUser):
    nickname = models.CharField(max_length=12, blank=True, null=True)
    verified = models.BooleanField(verbose_name=_('verified'), default=False)
    sent = models.DateTimeField(verbose_name=_('sent'), null=True)
    key = models.CharField(verbose_name=_('key'), max_length=64, unique=True)
    user_avatar = models.BooleanField(default=True)
    avatar_img = models.ImageField(
        blank=True, null=True, upload_to='avatar/', default='avatar/d_avatar.png')
    description = models.TextField(null=True, blank=True)
    address = models.CharField(max_length=50, null=True, blank=True)
    phone = models.CharField(max_length=11, null=True, blank=True)
    born_date = models.DateField(
        verbose_name=u'出生日期', null=True, blank=True, default=None)
    date_created = models.DateField(
        null=True, blank=True, verbose_name=u'账户创建日期', auto_now_add=True)
    favorite = models.ManyToManyField(
        Topic, verbose_name='fav_user', related_name='fav', blank=True)
    vote = models.ManyToManyField(
        Topic, verbose_name='vote_user', related_name='vote', blank=True)
    coins = models.IntegerField(default=0, blank=True, null=True)
    location = models.CharField(max_length=20, blank=True, null=True)
    last_activity = models.DateTimeField(auto_now_add=True)
    last_posttime = models.DateTimeField(auto_now_add=True)
    signature = models.CharField(
        max_length=128, default='This guy is lazy that nothing to leave')
    website = models.URLField(blank=True, null=True)

    def __unicode__(self):
        return '<userInfo: %s>' % self.user

    def unread_mention(self):
        return self.user.recevied_mentions.filter(read=False)

    def old_mention(self):
        return self.user.recevied_mentions.filter(read=True)[0:5]

    def username(self):
        if self.nickname:
            return self.nickname
        else:
            return self.user.usename

    def latest_activity(self):
        d = dict()
        d['topic'] = self.user.topics.all().filter(
            deleted=False).order_by('-time_created')[0:10]
        d['post'] = self.user.posts.all().filter(
            deleted=False).order_by('-time_created')[0:10]
        return d

    def get_fav_topic(self):
        return self.favorite.all()

    def get_fav_counts(self):
        return self.favorite.count()

    def get_topic_count(self):
        return self.user.topics.filter(replys=None).count()

    def get_reply_count(self):
        return self.user.topics.exclude(reply=None).count()

    def get_unread_replys(self):
        all_replys = []
        for topic in self.user.topics.filter(is_active=True, replys=None):
            replys = Topic.objects.filter(replys=topic, is_read=False)
            for reply in replys:
                all_replys.append(reply)
            return all_replys


class Social(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    access_token = models.CharField(max_length=255)
    openid = models.CharField(max_length=255)
    avatar = models.URLField()

    def __unicode__(self):
        return self.user.username
