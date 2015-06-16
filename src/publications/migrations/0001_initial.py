# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('portal', '0005_auto_20150615_2100'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publication',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(default=b'Note', max_length=20, choices=[(b'Note', 'Publication'), (b'Photo', 'Photogallery'), (b'Rss', 'Rss')])),
                ('slug', models.CharField(max_length=100, unique=True, null=True, blank=True)),
                ('rss_stream', models.IntegerField(null=True, blank=True)),
                ('rss_url', models.CharField(max_length=255, null=True, blank=True)),
                ('subcategory', models.ForeignKey(to='portal.MenuItem')),
            ],
        ),
        migrations.CreateModel(
            name='PublicationItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publication_date', models.DateTimeField(auto_now_add=True)),
                ('show_date', models.BooleanField(default=False)),
                ('state', models.CharField(default=b'N', max_length=5, choices=[(b'P', 'Published'), (b'H', 'Holded'), (b'N', 'Draft')])),
                ('title', models.CharField(max_length=100)),
                ('short_text', tinymce.models.HTMLField()),
                ('text', tinymce.models.HTMLField()),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('locale', models.ForeignKey(to='portal.Lang')),
                ('publication', models.ForeignKey(to='publications.Publication')),
            ],
        ),
        migrations.CreateModel(
            name='PublicationSubcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publication', models.ForeignKey(to='publications.Publication')),
                ('subcategory', models.ForeignKey(to='portal.MenuItem')),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='publication',
            unique_together=set([('rss_stream', 'rss_url')]),
        ),
    ]
