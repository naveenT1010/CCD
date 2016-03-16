# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0024_studentjobrelation_round'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentjobrelation',
            name='ppo_accepted',
        ),
        migrations.RemoveField(
            model_name='studentjobrelation',
            name='ppo_approved',
        ),
        migrations.RemoveField(
            model_name='studentjobrelation',
            name='ppo_init',
        ),
    ]
