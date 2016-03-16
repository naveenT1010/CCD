# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0026_auto_20160315_2240'),
    ]

    operations = [
        migrations.RenameField(
            model_name='studentjobrelation',
            old_name='shortlist_status',
            new_name='shortlist_init',
        ),
        migrations.AddField(
            model_name='studentjobrelation',
            name='shortlist_approved',
            field=models.NullBooleanField(default=None),
        ),
    ]
