# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Configuration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publications_page_size', models.IntegerField(default=6, verbose_name='News Page Size')),
            ],
        ),
        migrations.AlterField(
            model_name='publication',
            name='slug',
            field=models.CharField(max_length=100, null=True, unique_for_date=b'publication_date', blank=True),
        ),
        migrations.AlterField(
            model_name='publication',
            name='state',
            field=models.CharField(default=b'N', max_length=5, choices=[(b'I', 'Hidden'), (b'P', 'Published'), (b'H', 'Holded'), (b'N', 'Draft')]),
        ),
        migrations.AddField(
            model_name='configuration',
            name='last_old_publication',
            field=models.ForeignKey(blank=True, to='publications.Publication', null=True),
        ),
    ]
