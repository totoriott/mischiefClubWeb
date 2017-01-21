# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablesaltGame', '0003_auto_20160113_1430'),
    ]

    operations = [
        migrations.AddField(
            model_name='gamedata',
            name='discardPile',
            field=models.CharField(default=[], max_length=1000),
            preserve_default=False,
        ),
    ]
