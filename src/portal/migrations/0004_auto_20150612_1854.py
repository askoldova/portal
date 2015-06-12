# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0003_auto_20150612_1830'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mainmenu',
            options={'ordering': ('hidden', 'order', 'caption')},
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': ('menu__order', 'order', 'caption')},
        ),
        migrations.AlterField(
            model_name='menuitem',
            name='caption',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterUniqueTogether(
            name='menuitem',
            unique_together=set([('menu', 'caption', 'locale')]),
        ),
    ]
