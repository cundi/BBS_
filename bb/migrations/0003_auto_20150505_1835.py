# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb', '0002_auto_20150505_1822'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='avatar',
            field=models.ImageField(upload_to='deepinbbs/img/', null=True, verbose_name='\u677f\u5757\u5934\u50cf', blank=True),
        ),
    ]
