# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tripster', '0003_auto_20141205_2350'),
    ]

    operations = [
        migrations.CreateModel(
            name='TripRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('invitee', models.ForeignKey(to='tripster.TripsterUser')),
                ('trip', models.ForeignKey(to='tripster.Trip')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='triprequest',
            unique_together=set([('invitee', 'trip')]),
        ),
        migrations.AlterField(
            model_name='friendrequest',
            name='invitee',
            field=models.ForeignKey(related_name='friend_requests', to='tripster.TripsterUser'),
            preserve_default=True,
        ),
    ]
