# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Circle',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('statement', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='PendingRequest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('circle_name', models.CharField(max_length=100)),
                ('username', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('birthday', models.DateField(null=True)),
                ('sex', models.CharField(max_length=10, null=True)),
                ('phone_number', models.BigIntegerField(null=True)),
                ('nickname', models.CharField(max_length=100, null=True)),
                ('school', models.CharField(max_length=100, null=True)),
                ('grade', models.CharField(max_length=10, null=True)),
                ('school_id', models.BigIntegerField(null=True)),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='circle',
            name='profile',
            field=models.ManyToManyField(to='user_auth.Profile'),
        ),
    ]
