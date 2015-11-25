# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=1000)),
                ('thumb_up', models.BigIntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1000)),
                ('thumb_up', models.BigIntegerField(null=True)),
                ('circles', models.ManyToManyField(to='user_auth.Circle')),
                ('profile', models.ForeignKey(to='user_auth.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('follower', models.BigIntegerField(null=True)),
                ('followed', models.BigIntegerField(null=True)),
                ('direction', models.IntegerField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FollowSensor',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('whoto', models.BigIntegerField(null=True)),
                ('censor', models.BigIntegerField(null=True)),
            ],
        ),
        migrations.AddField(
            model_name='comment',
            name='content',
            field=models.ForeignKey(to='content.Content', null=True),
        ),
        migrations.AddField(
            model_name='comment',
            name='profile',
            field=models.ForeignKey(to='user_auth.Profile'),
        ),
    ]
