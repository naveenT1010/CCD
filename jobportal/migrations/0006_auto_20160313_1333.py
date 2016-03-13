# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0005_auto_20160313_1252'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.ForeignKey(to='jobportal.Year', null=True),
        ),
    ]
