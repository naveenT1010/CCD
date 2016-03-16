# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0028_globaladminsettings'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentjobrelation',
            name='dropped',
            field=models.BooleanField(default=False),
        ),
    ]
