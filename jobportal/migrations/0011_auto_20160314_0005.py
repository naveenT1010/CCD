# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jobportal.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0010_auto_20160313_1830'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='avatar',
            field=models.ImageField(null=True, upload_to=jobportal.models.generate_profilepic_name),
        ),
        migrations.AddField(
            model_name='student',
            name='signature',
            field=models.ImageField(null=True, upload_to=jobportal.models.generate_signature_name),
        ),
    ]
