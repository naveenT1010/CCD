# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0002_auto_20160317_1140'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indinternship',
            name='last_updated',
            field=models.DateTimeField(blank=True),
        ),
    ]
