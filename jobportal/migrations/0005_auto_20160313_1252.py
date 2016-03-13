# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0004_auto_20160313_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='programme',
            name='name',
            field=models.CharField(max_length=10, choices=[(b'BTECH', b'B.Tech.'), (b'MTECH', b'M.Tech.'), (b'PHD', b'Ph.D.')]),
        ),
    ]
