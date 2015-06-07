# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nickname', models.CharField(max_length=12, null=True, blank=True)),
                ('user_avatar', models.BooleanField(default=True)),
                ('avatar_img', models.ImageField(default='avatar/d_avatar.png', null=True, upload_to='avatar/', blank=True)),
                ('description', models.TextField(null=True, blank=True)),
                ('address', models.CharField(max_length=50, null=True, blank=True)),
                ('phone', models.CharField(max_length=11, null=True, blank=True)),
                ('born_date', models.DateField(default=None, null=True, verbose_name='\u51fa\u751f\u65e5\u671f', blank=True)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='\u8d26\u6237\u521b\u5efa\u65e5\u671f', null=True)),
                ('coins', models.IntegerField(default=0, null=True, blank=True)),
                ('location', models.CharField(max_length=20, null=True, blank=True)),
                ('last_activity', models.DateTimeField(auto_now_add=True)),
                ('last_posttime', models.DateTimeField(auto_now_add=True)),
                ('signature', models.CharField(default='This guy is lazy that nothing to leave', max_length=128)),
                ('website', models.URLField(null=True, blank=True)),
                ('favorite', models.ManyToManyField(related_name='fav', verbose_name='fav_user', to='bb.Topic', blank=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
                ('vote', models.ManyToManyField(related_name='vote', verbose_name='vote_user', to='bb.Topic', blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Social',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('access_token', models.CharField(max_length=255)),
                ('openid', models.CharField(max_length=255)),
                ('avatar', models.URLField()),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
