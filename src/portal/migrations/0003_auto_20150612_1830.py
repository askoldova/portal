# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0002_lang_default'),
    ]

    operations = [
        migrations.CreateModel(
            name='MainMenu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(unique=True, max_length=100)),
                ('order', models.SmallIntegerField(default=0)),
                ('hidden', models.BooleanField(default=False)),
                ('width', models.CharField(max_length=10, null=True, blank=True)),
                ('locale', models.ForeignKey(to='portal.Lang')),
            ],
        ),
        migrations.CreateModel(
            name='MainMenuI18n',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=100)),
                ('locale', models.ForeignKey(to='portal.Lang')),
                ('menu', models.ForeignKey(to='portal.MainMenu')),
            ],
            options={
                'ordering': ('menu__order', 'locale__code'),
            },
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(unique=True, max_length=100)),
                ('order', models.SmallIntegerField(default=0)),
                ('locale', models.ForeignKey(to='portal.Lang')),
                ('menu', models.ForeignKey(to='portal.MainMenu')),
            ],
            options={
                'ordering': ('order', 'caption'),
            },
        ),
        migrations.CreateModel(
            name='MenuItemI18n',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('caption', models.CharField(max_length=100)),
                ('locale', models.ForeignKey(to='portal.Lang')),
                ('menu', models.ForeignKey(to='portal.MainMenu')),
                ('menu_item', models.ForeignKey(to='portal.MenuItem')),
            ],
            options={
                'ordering': ('menu__order', 'locale__code'),
            },
        ),
        migrations.AlterUniqueTogether(
            name='langlocale',
            unique_together=set([('lang', 'locale')]),
        ),
        migrations.AlterUniqueTogether(
            name='menuitemi18n',
            unique_together=set([('menu', 'caption', 'locale'), ('menu_item', 'locale')]),
        ),
        migrations.AlterUniqueTogether(
            name='mainmenui18n',
            unique_together=set([('menu', 'locale'), ('menu', 'caption')]),
        ),
    ]
