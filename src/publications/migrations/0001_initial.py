# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models
import filebrowser.fields
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
                ('state', models.CharField(default=b'N', max_length=5, choices=[(b'P', 'Published'), (b'H', 'Holded'), (b'N', 'Draft')])),
                ('publication_date', models.DateField(db_index=True)),
                ('show_date', models.BooleanField(default=False)),
                ('slug', models.CharField(max_length=100, unique=True, null=True, unique_for_date=True, blank=True)),
                ('type', models.CharField(default=b'Note', max_length=20, choices=[(b'Note', 'Publication'), (b'Photo', 'Photogallery'), (b'Rss', 'Rss')])),
                ('title', models.CharField(max_length=256, null=True, blank=True)),
                ('short_text', tinymce.models.HTMLField()),
                ('text', tinymce.models.HTMLField(null=True, blank=True)),
                ('rss_url', models.CharField(max_length=255, null=True, blank=True)),
                ('old_id', models.IntegerField(db_index=True, null=True, blank=True)),
                ('author', models.ForeignKey(blank=True, to=settings.AUTH_USER_MODEL, null=True)),
                ('locale', models.ForeignKey(to='portal.Lang')),
            ],
            options={
                'ordering': ('-publication_date',),
            },
        ),
        migrations.CreateModel(
            name='PublicationImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file', filebrowser.fields.FileBrowseField(max_length=255)),
                ('caption', models.CharField(max_length=255, null=True, blank=True)),
                ('name', models.CharField(max_length=128, null=True, blank=True)),
                ('publication', models.ForeignKey(to='publications.Publication')),
            ],
            options={
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='PublicationSubcategory',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publication', models.ForeignKey(to='publications.Publication')),
                ('subcategory', models.ForeignKey(to='portal.MenuItem')),
            ],
        ),
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
        migrations.AddField(
            model_name='publication',
            name='rss_stream',
            field=models.ForeignKey(blank=True, to='publications.RssImportStream', null=True),
        ),
        migrations.AddField(
            model_name='publication',
            name='subcategory',
            field=models.ForeignKey(to='portal.MenuItem'),
        ),
        migrations.AlterUniqueTogether(
            name='publicationimage',
            unique_together=set([('publication', 'file')]),
        ),
        migrations.AlterUniqueTogether(
            name='publication',
            unique_together=set([('publication_date', 'slug'), ('rss_stream', 'rss_url')]),
        ),
        migrations.AlterIndexTogether(
            name='publication',
            index_together=set([('state', 'publication_date'), ('state', 'subcategory', 'publication_date')]),
        ),
    ]
