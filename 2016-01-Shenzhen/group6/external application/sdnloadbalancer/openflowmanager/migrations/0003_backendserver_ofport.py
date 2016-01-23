# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openflowmanager', '0002_clientinfo'),
    ]

    operations = [
        migrations.AddField(
            model_name='backendserver',
            name='ofport',
            field=models.CharField(default=1, max_length=60),
            preserve_default=False,
        ),
    ]
