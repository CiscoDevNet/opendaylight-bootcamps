# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openflowmanager', '0003_backendserver_ofport'),
    ]

    operations = [
        migrations.CreateModel(
            name='VirtualService',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('virtual_ip', models.CharField(max_length=60)),
                ('virtual_port', models.CharField(max_length=60)),
                ('vport', models.CharField(max_length=60)),
                ('l4_protocol', models.CharField(max_length=60)),
                ('bs_pool', models.CharField(max_length=60)),
            ],
        ),
        migrations.DeleteModel(
            name='VirtualIP',
        ),
    ]
