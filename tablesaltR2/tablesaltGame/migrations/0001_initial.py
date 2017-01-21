# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BoostCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('textDescription', models.CharField(default=b'no description', max_length=500)),
                ('abilityType', models.IntegerField(default=1, choices=[(1, b'None'), (2, b'Cheer Collab'), (3, b'Cheer Solo'), (4, b'Bet Solo'), (5, b'Bet Boost'), (6, b'Bet Balance'), (7, b'Reversal'), (8, b'Underdog'), (9, b'Mimic')])),
                ('cheerAmount', models.IntegerField(default=0)),
                ('betAmount', models.IntegerField(default=0)),
                ('enabled', models.BooleanField(default=True)),
                ('copiesOfCard', models.IntegerField(default=1)),
            ],
        ),
        migrations.CreateModel(
            name='CompetitorCard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('textDescription', models.CharField(default=b'no description', max_length=500)),
                ('betTrackValues', models.CharField(max_length=500)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameConfiguration',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('numberOfMatches', models.IntegerField(default=5)),
                ('charactersPerMatch', models.IntegerField(default=3)),
                ('numberOfPlayers', models.IntegerField(default=4)),
                ('handSize', models.IntegerField(default=6)),
                ('discardDownHandSizeAfterMatch', models.IntegerField(default=3)),
                ('betTrackValues', models.CharField(max_length=500)),
                ('randomizerValues', models.CharField(max_length=500)),
                ('enabled', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='GameData',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('public', models.BooleanField(default=False)),
                ('creationTime', models.DateTimeField(default=django.utils.timezone.now)),
                ('passcode', models.CharField(default=b'', max_length=10000)),
                ('notes', models.CharField(default=b'', max_length=1000, blank=True)),
                ('configurationId', models.IntegerField(default=1)),
                ('randomSeed', models.CharField(max_length=10000)),
                ('competitorCardTopIndex', models.IntegerField(default=10)),
                ('competitorCardDeck', models.CharField(max_length=1000)),
                ('boostTopIndex', models.IntegerField(default=0)),
                ('boostCardDeck', models.CharField(max_length=1000)),
                ('currentMatch', models.IntegerField(default=0)),
                ('serializedPlayers', models.CharField(max_length=10000)),
                ('serializedMatches', models.CharField(max_length=10000)),
                ('dataVersion', models.IntegerField(default=0)),
            ],
        ),
    ]
