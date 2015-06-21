# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filebrowser.fields


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0001_initial'),
    ]

    operations = [
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
        migrations.AlterField(
            model_name='publicationitem',
            name='title',
            field=models.CharField(max_length=256),
        ),
        migrations.AlterUniqueTogether(
            name='publicationimage',
            unique_together=set([('publication', 'file')]),
        ),
    ]
