# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('url', models.CharField(max_length=200)),
                ('album', models.ForeignKey(to='tripster.Album')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContentComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=2000)),
                ('rating', models.IntegerField()),
                ('content', models.ForeignKey(to='tripster.Content')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TripComment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('comment', models.CharField(max_length=2000)),
                ('rating', models.IntegerField()),
                ('trip', models.ForeignKey(to='tripster.Trip')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TripsterUser',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('affiliation', models.CharField(max_length=100)),
                ('dream_location', models.ManyToManyField(to='tripster.Location')),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='tripster.TripsterUser')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='tripcomment',
            name='user',
            field=models.ForeignKey(to='tripster.TripsterUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trip',
            name='host',
            field=models.ForeignKey(related_name='host', to='tripster.TripsterUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trip',
            name='locations',
            field=models.ManyToManyField(to='tripster.Location'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='trip',
            name='participants',
            field=models.ManyToManyField(related_name='participants', to='tripster.TripsterUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contentcomment',
            name='user',
            field=models.ForeignKey(to='tripster.TripsterUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='album',
            name='trip',
            field=models.ForeignKey(to='tripster.Trip'),
            preserve_default=True,
        ),
    ]
