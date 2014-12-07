# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tripster', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='FriendRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invitee', models.ForeignKey(related_name='requests', to='tripster.TripsterUser')),
                ('user', models.ForeignKey(to='tripster.TripsterUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='trip',
            name='name',
            field=models.CharField(default='asdf', max_length=200),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='trip',
            name='host',
            field=models.ForeignKey(to='tripster.TripsterUser'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='trip',
            name='participants',
            field=models.ManyToManyField(related_name='trips', to='tripster.TripsterUser'),
            preserve_default=True,
        ),
    ]
