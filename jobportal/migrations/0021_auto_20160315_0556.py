# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0020_auto_20160315_0555'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='department',
            unique_together=set([('dept_code', 'year')]),
        ),
    ]
