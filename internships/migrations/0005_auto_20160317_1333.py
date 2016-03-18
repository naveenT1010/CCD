# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0004_auto_20160317_1332'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indinternship',
            name='approved_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='indinternship',
            name='last_updated',
            field=models.DateTimeField(),
        ),
    ]
