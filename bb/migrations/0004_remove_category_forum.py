# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb', '0003_auto_20150507_1710'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='category',
            name='forum',
        ),
    ]
