# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='forumprofile',
            name='user',
        ),
        migrations.AddField(
            model_name='forumprofile',
            name='key',
            field=models.CharField(default=1, unique=True, max_length=64, verbose_name='key'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='forumprofile',
            name='last_login',
            field=models.DateTimeField(null=True, verbose_name='last login', blank=True),
        ),
        migrations.AddField(
            model_name='forumprofile',
            name='password',
            field=models.CharField(default='1', max_length=128, verbose_name='password'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='forumprofile',
            name='sent',
            field=models.DateTimeField(null=True, verbose_name='sent'),
        ),
        migrations.AddField(
            model_name='forumprofile',
            name='verified',
            field=models.BooleanField(default=False, verbose_name='verified'),
        ),
    ]
