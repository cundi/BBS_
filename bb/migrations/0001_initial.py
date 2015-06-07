# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import DjangoUeditor.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Appendix',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('content', models.TextField()),
                ('content_rendered', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=40)),
                ('description', models.TextField(null=True, blank=True)),
                ('hidden', models.NullBooleanField(default=False, help_text='\u5982\u679c\u9009\u4e2d\uff0c\u8be5\u677f\u5757\u53ea\u5bf9\u7ad9\u70b9\u6ce8\u518cadmin\u53ef\u89c1')),
                ('position', models.IntegerField(default=0, verbose_name='Position', blank=True)),
                ('category_admin', models.ManyToManyField(related_name='category_admin', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['title'],
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Forum',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=200)),
                ('avatar', models.ImageField(upload_to=b'', null=True, verbose_name='\u677f\u5757\u5934\u50cf', blank=True)),
                ('description', models.CharField(max_length=300, null=True, blank=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='creation date and time')),
                ('post_count', models.IntegerField(default=0, verbose_name='\u56de\u5e16\u8ba1\u6570', blank=True)),
                ('topic_count', models.IntegerField(default=0, verbose_name='\u5e16\u5b50\u8ba1\u6570', blank=True)),
                ('hidden', models.BooleanField(default=False, verbose_name='\u5206\u533a\u662f\u5426\u9690\u85cf')),
                ('category', models.ForeignKey(verbose_name='Category', blank=True, to='bb.Category', null=True)),
                ('forum_admin', models.ForeignKey(related_name='manager', verbose_name='\u7248\u4e3b', blank=True, to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(related_name='child_forums', verbose_name='Parent forum', blank=True, to='bb.Forum', null=True)),
            ],
            options={
                'verbose_name': 'Forum',
                'verbose_name_plural': 'Forums',
            },
        ),
        migrations.CreateModel(
            name='Mention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('read', models.BooleanField(default=False)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-time_created'],
            },
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', models.TextField(null=True, blank=True)),
                ('read', models.BooleanField(default=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('receiver', models.ForeignKey(related_name='received_nofitications', to=settings.AUTH_USER_MODEL)),
                ('sender', models.ForeignKey(related_name='sent_notifications', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('content', DjangoUeditor.models.UEditorField(blank=True)),
                ('time_created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('updated', models.DateTimeField(null=True, verbose_name='\u56de\u5e16\u6700\u540e\u7f16\u8f91\u65f6\u95f4', blank=True)),
                ('user_ip', models.GenericIPAddressField(default='0.0.0.0', null=True, verbose_name='\u53d1\u5e16\u4ebaIP\u5730\u5740')),
                ('deleted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['time_created'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, null=True, blank=True)),
                ('content', DjangoUeditor.models.UEditorField(verbose_name='\u5185\u5bb9', blank=True)),
                ('content_rendered', models.TextField(null=True, blank=True)),
                ('view_count', models.IntegerField(default=0)),
                ('reply_count', models.IntegerField(default=0)),
                ('last_replied_time', models.DateTimeField(null=True, blank=True)),
                ('time_created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now_add=True)),
                ('is_active', models.BooleanField(default=True)),
                ('is_read', models.BooleanField(default=False)),
                ('is_top', models.BooleanField(default=False)),
                ('order', models.IntegerField(default=10)),
                ('deleted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('forum', models.ForeignKey(verbose_name='forum of topic', to='bb.Forum')),
                ('subscribers', models.ManyToManyField(related_name='subscriptions', verbose_name='\u8ba2\u9605\u4eba', to=settings.AUTH_USER_MODEL, blank=True)),
            ],
            options={
                'ordering': ['order', '-time_created'],
            },
        ),
        migrations.AddField(
            model_name='post',
            name='topic',
            field=models.ForeignKey(to='bb.Topic'),
        ),
        migrations.AddField(
            model_name='notification',
            name='topic',
            field=models.ForeignKey(blank=True, to='bb.Topic', null=True),
        ),
        migrations.AddField(
            model_name='mention',
            name='post',
            field=models.ForeignKey(blank=True, to='bb.Post', null=True),
        ),
        migrations.AddField(
            model_name='mention',
            name='receiver',
            field=models.ForeignKey(related_name='received_mentions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mention',
            name='sender',
            field=models.ForeignKey(related_name='sent_mentions', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='mention',
            name='topic',
            field=models.ForeignKey(blank=True, to='bb.Topic', null=True),
        ),
        migrations.AddField(
            model_name='appendix',
            name='topic',
            field=models.ForeignKey(to='bb.Topic'),
        ),
    ]
