# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0016_auto_20160315_0340'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='open_for_alum',
        ),
        migrations.RemoveField(
            model_name='job',
            name='open_for_studs',
        ),
    ]
