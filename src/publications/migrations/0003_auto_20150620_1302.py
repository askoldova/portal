# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_auto_20150620_1258'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationitem',
            name='text',
            field=tinymce.models.HTMLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='publicationitem',
            name='title',
            field=models.CharField(max_length=256, null=True, blank=True),
        ),
    ]
