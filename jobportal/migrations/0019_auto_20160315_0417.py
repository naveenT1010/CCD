# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0018_auto_20160315_0412'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='bond',
            field=models.NullBooleanField(default=None),
        ),
        migrations.AlterField(
            model_name='job',
            name='num_openings',
            field=models.DecimalField(default=20, null=True, max_digits=3, decimal_places=0),
        ),
    ]
