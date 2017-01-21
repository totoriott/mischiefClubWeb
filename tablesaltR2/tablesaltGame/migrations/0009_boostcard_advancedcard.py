# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablesaltGame', '0008_competitorcard_shortname'),
    ]

    operations = [
        migrations.AddField(
            model_name='boostcard',
            name='advancedCard',
            field=models.BooleanField(default=False),
        ),
    ]
