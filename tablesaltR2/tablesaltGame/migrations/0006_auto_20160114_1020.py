# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablesaltGame', '0005_remove_gamedata_currentmatch'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamedata',
            name='randomSeed',
        ),
        migrations.AlterField(
            model_name='boostcard',
            name='abilityType',
            field=models.IntegerField(default=0, choices=[(0, b'None'), (2, b'Cheer Collab'), (3, b'Cheer Solo'), (4, b'Bet Solo'), (5, b'Bet Boost'), (6, b'Bet Balance'), (7, b'Reversal'), (8, b'Underdog'), (9, b'Mimic')]),
        ),
    ]
