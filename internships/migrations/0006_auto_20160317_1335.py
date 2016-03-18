# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0005_auto_20160317_1333'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programmeinternrelation',
            name='dept',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'year', to='jobportal.Department', chained_field=b'year', null=True),
        ),
        migrations.AlterField(
            model_name='programmeinternrelation',
            name='prog',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'dept', to='jobportal.Programme', chained_field=b'dept', null=True),
        ),
    ]
