# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tablesaltGame', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='competitorcard',
            old_name='betTrackValues',
            new_name='cheerTrackValues',
        ),
    ]