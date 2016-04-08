# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0006_auto_20160317_1335'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentinternrelation',
            name='ppo_approved',
            field=models.NullBooleanField(default=None),
        ),
    ]
