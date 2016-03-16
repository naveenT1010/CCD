# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0022_auto_20160315_0558'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentjobrelation',
            name='cv_field',
        ),
    ]
