# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('openflowmanager', '0004_auto_20160122_1139'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='virtualservice',
            name='vport',
        ),
    ]
