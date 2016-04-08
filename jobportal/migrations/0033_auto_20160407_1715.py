# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0032_auto_20160407_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='minimum_cpi',
            field=models.DecimalField(default=4.0, max_digits=4, decimal_places=2, blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='num_openings',
            field=models.DecimalField(default=10, null=True, max_digits=3, decimal_places=0),
        ),
        migrations.AlterField(
            model_name='job',
            name='percentage_x',
            field=models.DecimalField(default=70.0, null=True, max_digits=5, decimal_places=2),
        ),
        migrations.AlterField(
            model_name='job',
            name='percentage_xii',
            field=models.DecimalField(default=70.0, null=True, max_digits=5, decimal_places=2),
        ),
    ]
