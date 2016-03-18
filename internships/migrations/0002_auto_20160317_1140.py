# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='indinternship',
            old_name='stipned',
            new_name='stipend',
        ),
    ]
