# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0003_auto_20160313_0121'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='organization_type',
            field=models.CharField(default=b'PSU', max_length=20, verbose_name=b'Type of Organization', blank=True, choices=[(b'Private', b'Private'), (b'Government', b'Government'), (b'PSU', b'PSU'), (b'MNC(Indian Origin)', b'MNC(Indian Origin)'), (b'MNC(Foreign Origin)', b'MNC(Foreign Origin)'), (b'NGO', b'NGO'), (b'Other', b'Other')]),
        ),
        migrations.AlterField(
            model_name='companyreg',
            name='organization_type_reg',
            field=models.CharField(default=b'PSU', max_length=20, verbose_name=b'Type of Organization', blank=True, choices=[(b'Private', b'Private'), (b'Government', b'Government'), (b'PSU', b'PSU'), (b'MNC(Indian Origin)', b'MNC(Indian Origin)'), (b'MNC(Foreign Origin)', b'MNC(Foreign Origin)'), (b'NGO', b'NGO'), (b'Other', b'Other')]),
        ),
        migrations.AlterField(
            model_name='student',
            name='dept',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'year', to='jobportal.Department', chained_field=b'year'),
        ),
        migrations.AlterField(
            model_name='student',
            name='nationality',
            field=models.CharField(default=b'INDIAN', max_length=15, blank=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='prog',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'dept', to='jobportal.Programme', chained_field=b'dept'),
        ),
        migrations.AlterField(
            model_name='student',
            name='year',
            field=models.ForeignKey(to='jobportal.Year'),
        ),
    ]
