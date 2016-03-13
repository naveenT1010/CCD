# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0009_auto_20160313_1707'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='first_hr_designation',
            field=models.CharField(default=b'First HR', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='first_hr_email',
            field=models.CharField(default=b'firsthr@xyz.com', max_length=60, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='first_hr_fax',
            field=models.CharField(default=b'0123456', max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='first_hr_mobile',
            field=models.CharField(default=b'0123456789', max_length=12, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='first_hr_name',
            field=models.CharField(default=b'Mr. First HR', max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_designation',
            field=models.CharField(default=b'Head HR', max_length=30, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_email',
            field=models.CharField(default=b'headhr@xyz.com', max_length=60, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_fax',
            field=models.CharField(default=b'0123456', max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_mobile',
            field=models.CharField(default=b'0123456789', max_length=12, blank=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='head_hr_name',
            field=models.CharField(default=b'Mr. Head HR', max_length=20, blank=True),
        ),
    ]
