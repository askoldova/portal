# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20150615_2100'),
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='publication',
            name='subcategory',
            field=models.ForeignKey(to='portal.MenuItem'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='publication',
            name='rss_stream',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='rss_url',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='slug',
            field=models.CharField(max_length=100, unique=True, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publicationitem',
            name='author',
            field=models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True),
        ),
    ]
