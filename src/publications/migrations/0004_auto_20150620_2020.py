# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0003_auto_20150620_1302'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publicationitem',
            name='publication_date',
            field=models.DateTimeField(),
        ),
    ]
