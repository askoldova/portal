# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0005_auto_20150615_2100'),
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RssImportStream',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('enabled', models.BooleanField(default=True)),
                ('rss_url', models.CharField(max_length=256)),
                ('pool_period_mins', models.IntegerField(default=30)),
                ('next_pool', models.DateTimeField()),
                ('link_caption', models.CharField(max_length=255)),
                ('language', models.ForeignKey(to='portal.Lang')),
                ('menu_item', models.ForeignKey(to='portal.MenuItem')),
            ],
        ),
        migrations.AlterField(
            model_name='publication',
            name='rss_stream',
            field=models.ForeignKey(blank=True, to='publications.RssImportStream', null=True),
        ),
    ]
