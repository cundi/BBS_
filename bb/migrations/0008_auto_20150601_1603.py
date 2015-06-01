# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import DjangoUeditor.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('bb', '0007_auto_20150519_2153'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='content_rendered',
        ),
        migrations.RemoveField(
            model_name='forum',
            name='forum_admin',
        ),
        migrations.AddField(
            model_name='forum',
            name='forum_admin',
            field=models.ForeignKey(related_name='manager', default=1, verbose_name='\u7248\u4e3b', blank=True, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='post',
            name='content',
            field=DjangoUeditor.models.UEditorField(verbose_name='\u5185\u5bb9', blank=True),
        ),
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=DjangoUeditor.models.UEditorField(verbose_name='\u5185\u5bb9', blank=True),
        ),
    ]
