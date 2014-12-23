# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_auto_20141122_0942'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='preferred',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
