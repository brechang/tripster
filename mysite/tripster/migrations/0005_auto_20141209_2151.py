# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tripster', '0004_auto_20141207_0100'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContentRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
                ('content', models.ForeignKey(to='tripster.Content')),
                ('user', models.ForeignKey(to='tripster.TripsterUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TripRating',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('rating', models.IntegerField()),
                ('trip', models.ForeignKey(to='tripster.Trip')),
                ('user', models.ForeignKey(to='tripster.TripsterUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='contentcomment',
            name='rating',
        ),
        migrations.RemoveField(
            model_name='tripcomment',
            name='rating',
        ),
    ]
