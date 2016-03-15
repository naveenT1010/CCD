# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jobportal.models


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0012_auto_20160314_0016'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='avatar',
            field=models.ImageField(default=b'media/avatar/sample_avatar.png', upload_to=jobportal.models.generate_profilepic_name),
        ),
    ]
