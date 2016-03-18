# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('jobportal', '0029_studentjobrelation_dropped'),
    ]

    operations = [
        migrations.CreateModel(
            name='IndInternship',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('description', models.CharField(max_length=200)),
                ('designation', models.CharField(max_length=20)),
                ('profile', models.CharField(max_length=10)),
                ('stipned', models.IntegerField()),
                ('duration', models.IntegerField()),
                ('posted_on', models.DateTimeField()),
                ('last_updated', models.DateTimeField()),
                ('approved', models.NullBooleanField(default=None)),
                ('approved_on', models.DateTimeField()),
                ('opening_date', models.DateTimeField()),
                ('closing_date', models.DateTimeField()),
                ('company_owner', models.ForeignKey(to='jobportal.Company')),
            ],
        ),
        migrations.CreateModel(
            name='ProgrammeInternRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('dept', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'year', to='jobportal.Department', chained_field=b'year')),
                ('intern', models.ForeignKey(to='internships.IndInternship')),
                ('prog', smart_selects.db_fields.ChainedForeignKey(chained_model_field=b'dept', to='jobportal.Programme', chained_field=b'dept')),
                ('year', models.ForeignKey(to='jobportal.Year', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='StudentInternRelation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('round', models.IntegerField(default=1)),
                ('shortlist_init', models.BooleanField(default=False)),
                ('shortlist_approved', models.NullBooleanField(default=None)),
                ('intern_init', models.BooleanField(default=False)),
                ('intern_approved', models.NullBooleanField(default=None)),
                ('ppo_init', models.BooleanField(default=False)),
                ('ppo_approved', models.BooleanField(default=False)),
                ('dropped', models.BooleanField(default=False)),
                ('cv1', models.BooleanField(default=False)),
                ('cv2', models.BooleanField(default=False)),
                ('intern', models.ForeignKey(to='internships.IndInternship')),
                ('stud', models.ForeignKey(to='jobportal.Student')),
            ],
        ),
    ]
