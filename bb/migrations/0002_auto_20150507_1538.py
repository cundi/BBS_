# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='forum',
            field=models.ForeignKey(related_name='child_f', blank=True, to='bb.Forum', null=True),
        ),
        migrations.AlterField(
            model_name='forum',
            name='avatar',
            field=models.ImageField(upload_to='deepinbbs/img/', null=True, verbose_name='\u677f\u5757\u5934\u50cf', blank=True),
        ),
        migrations.AlterField(
            model_name='forum',
            name='created',
            field=models.DateTimeField(auto_now_add=True, verbose_name='creation date and time'),
        ),
    ]
