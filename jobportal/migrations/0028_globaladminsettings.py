# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0027_auto_20160316_0011'),
    ]

    operations = [
        migrations.CreateModel(
            name='GlobalAdminSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('CV_deadline', models.DateField(null=True)),
                ('profile_deadline', models.DateField(null=True)),
            ],
        ),
    ]
