# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BackendServer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ipaddr', models.CharField(max_length=60)),
                ('macaddr', models.CharField(max_length=60)),
            ],
        ),
        migrations.CreateModel(
            name='VirtualIP',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('pro', models.CharField(max_length=60)),
                ('virtual_ip', models.CharField(max_length=60)),
                ('virtual_port', models.CharField(max_length=60)),
            ],
        ),
    ]
