# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import versatileimagefield.fields
import jobportal.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0033_auto_20160407_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='signature',
            field=versatileimagefield.fields.VersatileImageField(default=b'avatar/sample_sign.png', upload_to=jobportal.models.generate_signature_name, blank=True),
        ),
    ]
