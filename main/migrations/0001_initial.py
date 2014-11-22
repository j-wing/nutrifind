# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('calories', models.IntegerField()),
                ('total_fat', models.IntegerField()),
                ('total_carbs', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
