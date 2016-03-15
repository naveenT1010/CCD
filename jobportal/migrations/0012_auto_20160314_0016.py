# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jobportal.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0011_auto_20160314_0005'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.ImageField(default=b'/avatar/sample_avatar.png', upload_to=jobportal.models.generate_profilepic_name),
        ),
    ]
