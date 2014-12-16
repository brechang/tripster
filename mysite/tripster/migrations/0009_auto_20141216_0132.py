# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tripster', '0008_auto_20141216_0117'),
    ]

    operations = [
        migrations.AddField(
            model_name='album',
            name='privacy',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='privacy',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trip',
            name='privacy',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tripsteruser',
            name='privacy',
            field=models.IntegerField(default=1),
            preserve_default=True,
        ),
    ]
