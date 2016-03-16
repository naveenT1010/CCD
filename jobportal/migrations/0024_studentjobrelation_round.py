# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0023_remove_studentjobrelation_cv_field'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentjobrelation',
            name='round',
            field=models.IntegerField(default=1),
        ),
    ]
