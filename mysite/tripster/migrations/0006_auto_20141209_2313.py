# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('tripster', '0005_auto_20141209_2151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='album',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='content',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='contentcomment',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='trip',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AlterModelOptions(
            name='tripcomment',
            options={'ordering': ['-timestamp']},
        ),
        migrations.AddField(
            model_name='album',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='content',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentcomment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trip',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='tripcomment',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='contentrating',
            unique_together=set([('user', 'content')]),
        ),
        migrations.AlterUniqueTogether(
            name='triprating',
            unique_together=set([('user', 'trip')]),
        ),
    ]
