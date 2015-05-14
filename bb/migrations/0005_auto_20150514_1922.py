# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb', '0004_remove_category_forum'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='category',
            field=models.ForeignKey(verbose_name='Category', blank=True, to='bb.Category', null=True),
        ),
    ]
