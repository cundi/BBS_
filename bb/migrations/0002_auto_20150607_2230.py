# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bb', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='topic',
            name='content_rendered',
        ),
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.CharField(default='1', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='forum',
            name='slug',
            field=models.CharField(default='1', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='post',
            name='slug',
            field=models.CharField(default='1', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='topic',
            name='slug',
            field=models.CharField(default='1', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='forum',
            name='hidden',
            field=models.BooleanField(default=2, verbose_name='\u5206\u533a\u662f\u5426\u9690\u85cf', choices=[(1, True), (2, False)]),
        ),
        migrations.AlterField(
            model_name='post',
            name='deleted',
            field=models.BooleanField(default=2, choices=[(1, True), (2, False)]),
        ),
        migrations.AlterField(
            model_name='topic',
            name='deleted',
            field=models.BooleanField(default=2, choices=[(1, True), (2, False)]),
        ),
        migrations.AlterField(
            model_name='topic',
            name='is_active',
            field=models.BooleanField(default=1, choices=[(1, True), (2, False)]),
        ),
        migrations.AlterField(
            model_name='topic',
            name='is_read',
            field=models.BooleanField(default=2, choices=[(1, True), (2, False)]),
        ),
        migrations.AlterField(
            model_name='topic',
            name='is_top',
            field=models.BooleanField(default=False, choices=[(1, True), (2, False)]),
        ),
    ]
