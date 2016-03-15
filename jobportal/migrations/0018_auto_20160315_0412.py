# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0017_auto_20160315_0342'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProgrammeJobRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dept', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'year', to='jobportal.Department', chained_field=b'year', null=True)),
            ],
        ),
        migrations.AlterField(
            model_name='job',
            name='cpi_shortlist',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='job',
            name='posted_by_alumnus',
            field=models.NullBooleanField(default=None, verbose_name=b'Posted by Alum'),
        ),
        migrations.AlterField(
            model_name='job',
            name='posted_by_company',
            field=models.NullBooleanField(default=None, verbose_name=b'Posted by Company'),
        ),
        migrations.AddField(
            model_name='programmejobrelation',
            name='job',
            field=models.ForeignKey(to='jobportal.Job'),
        ),
        migrations.AddField(
            model_name='programmejobrelation',
            name='prog',
            field=smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'dept', to='jobportal.Programme', chained_field=b'dept', null=True),
        ),
        migrations.AddField(
            model_name='programmejobrelation',
            name='year',
            field=models.ForeignKey(to='jobportal.Year', null=True),
        ),
    ]
