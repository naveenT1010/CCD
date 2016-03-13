# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0006_auto_20160313_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='company_count',
            field=models.DecimalField(default=0, null=True, max_digits=30, decimal_places=0, blank=True),
        ),
    ]
