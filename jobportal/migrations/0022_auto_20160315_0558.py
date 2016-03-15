# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0021_auto_20160315_0556'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='programme',
            unique_together=set([('year', 'dept', 'name')]),
        ),
    ]
