# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb', '0002_auto_20150507_1538'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='category',
            field=models.ForeignKey(related_name='forums', verbose_name='Category', blank=True, to='bb.Category', null=True),
        ),
    ]
