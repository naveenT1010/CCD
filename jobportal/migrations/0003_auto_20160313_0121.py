# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0002_auto_20160312_2301'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='companyreg',
            name='second_hr_designation_reg',
        ),
        migrations.RemoveField(
            model_name='companyreg',
            name='second_hr_email_reg',
        ),
        migrations.RemoveField(
            model_name='companyreg',
            name='second_hr_fax_reg',
        ),
        migrations.RemoveField(
            model_name='companyreg',
            name='second_hr_mobile_reg',
        ),
        migrations.RemoveField(
            model_name='companyreg',
            name='second_hr_name_reg',
        ),
    ]
