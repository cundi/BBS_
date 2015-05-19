# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb', '0005_auto_20150514_1922'),
    ]

    operations = [
        migrations.AlterField(
            model_name='forum',
            name='avatar',
            field=models.ImageField(upload_to=b'', null=True, verbose_name='\u677f\u5757\u5934\u50cf', blank=True),
        ),
    ]
