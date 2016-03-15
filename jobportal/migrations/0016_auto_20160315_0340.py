# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0015_auto_20160314_0149'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='alums',
        ),
        migrations.RemoveField(
            model_name='job',
            name='current_year',
        ),
        migrations.RemoveField(
            model_name='job',
            name='dept',
        ),
        migrations.RemoveField(
            model_name='job',
            name='prog',
        ),
        migrations.RemoveField(
            model_name='job',
            name='students',
        ),
    ]
