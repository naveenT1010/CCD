# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='second_hr_designation',
        ),
        migrations.RemoveField(
            model_name='company',
            name='second_hr_email',
        ),
        migrations.RemoveField(
            model_name='company',
            name='second_hr_fax',
        ),
        migrations.RemoveField(
            model_name='company',
            name='second_hr_mobile',
        ),
        migrations.RemoveField(
            model_name='company',
            name='second_hr_name',
        ),
    ]
