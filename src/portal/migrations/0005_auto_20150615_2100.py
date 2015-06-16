# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0004_auto_20150612_1854'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lang',
            options={'ordering': ('-default', 'caption')},
        ),
        migrations.AlterModelOptions(
            name='menuitem',
            options={'ordering': ('menu__hidden', 'menu__order', 'order', 'caption')},
        ),
    ]
