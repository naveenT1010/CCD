# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import versatileimagefield.fields
import jobportal.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0029_studentjobrelation_dropped'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=versatileimagefield.fields.VersatileImageField(default=b'avatar/sample_avatar.png', upload_to=jobportal.models.generate_profilepic_name, blank=True),
        ),
    ]
