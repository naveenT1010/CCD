# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0003_auto_20160317_1330'),
    ]

    operations = [
        migrations.AlterField(
            model_name='indinternship',
            name='last_updated',
            field=models.DateTimeField(null=True),
        ),
    ]
