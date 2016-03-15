# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0019_auto_20160315_0417'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='dept_code',
            field=models.CharField(max_length=4),
        ),
    ]
