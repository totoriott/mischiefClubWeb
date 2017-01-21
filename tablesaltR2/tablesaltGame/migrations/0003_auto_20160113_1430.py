# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablesaltGame', '0002_auto_20160113_1416'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamedata',
            name='boostTopIndex',
        ),
        migrations.RemoveField(
            model_name='gamedata',
            name='competitorCardTopIndex',
        ),
    ]
