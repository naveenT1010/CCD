# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0030_auto_20160317_1152'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='bond_link',
            field=models.URLField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='job',
            name='profile_name',
            field=models.CharField(default=b'SDE', max_length=15),
        ),
    ]
