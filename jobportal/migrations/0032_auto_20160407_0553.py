# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0031_auto_20160407_0553'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='profile_name',
            field=models.CharField(max_length=15, null=True),
        ),
    ]
