# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tripster', '0002_auto_20141205_2328'),
    ]

    operations = [
        migrations.AlterField(
            model_name='location',
            name='name',
            field=models.CharField(unique=True, max_length=100),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='album',
            unique_together=set([('name', 'trip')]),
        ),
        migrations.AlterUniqueTogether(
            name='content',
            unique_together=set([('album', 'name')]),
        ),
        migrations.AlterUniqueTogether(
            name='friendrequest',
            unique_together=set([('user', 'invitee')]),
        ),
        migrations.AlterUniqueTogether(
            name='trip',
            unique_together=set([('host', 'name')]),
        ),
    ]
