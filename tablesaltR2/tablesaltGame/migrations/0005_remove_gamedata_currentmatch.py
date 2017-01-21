# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablesaltGame', '0004_gamedata_discardpile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamedata',
            name='currentMatch',
        ),
    ]
