# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablesaltGame', '0007_auto_20160117_1752'),
    ]

    operations = [
        migrations.AddField(
            model_name='competitorcard',
            name='shortName',
            field=models.CharField(default='ok', max_length=20),
            preserve_default=False,
        ),
    ]
