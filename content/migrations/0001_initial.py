# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('text', models.CharField(max_length=1000)),
                ('circles', models.ManyToManyField(to='user_auth.Circle')),
                ('profile', models.ForeignKey(to='user_auth.Profile')),
            ],
        ),
    ]
