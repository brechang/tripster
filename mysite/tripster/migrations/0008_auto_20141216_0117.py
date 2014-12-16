# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tripster', '0007_auto_20141209_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tripsteruser',
            name='age',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tripsteruser',
            name='gender',
            field=models.CharField(default='None', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='tripsteruser',
            name='url',
            field=models.CharField(default='', max_length=200),
            preserve_default=False,
        ),
    ]
