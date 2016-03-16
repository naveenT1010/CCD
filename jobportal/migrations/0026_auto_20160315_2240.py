# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0025_auto_20160315_2238'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='alumjobrelation',
            name='cv_field',
        ),
        migrations.RemoveField(
            model_name='alumjobrelation',
            name='ppo_accepted',
        ),
        migrations.RemoveField(
            model_name='alumjobrelation',
            name='ppo_approved',
        ),
        migrations.RemoveField(
            model_name='alumjobrelation',
            name='ppo_init',
        ),
    ]
