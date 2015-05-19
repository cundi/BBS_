# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('bb', '0006_auto_20150519_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='content',
            field=froala_editor.fields.FroalaField(),
        ),
        migrations.AlterField(
            model_name='topic',
            name='forum',
            field=models.ForeignKey(verbose_name='forum of topic', to='bb.Forum'),
        ),
    ]
