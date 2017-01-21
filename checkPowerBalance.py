#!/usr/bin/env python
import random;
import pprint;
from operator import itemgetter;
import math;

abilityBoostDeck = 	[0, 1, 1, 2, 4];

ENUM_WIN = 0;
ENUM_DRAW = 1;
ENUM_LOSE = 2;

def doBattle(powerDiff):
	yourPower = powerDiff;
	theirPower = 0;

	random.shuffle(abilityBoostDeck);
	yourPower += abilityBoostDeck[0];
	theirPower += abilityBoostDeck[1];
	if (yourPower > theirPower):
		return ENUM_WIN;
	elif (yourPower < theirPower):
		return ENUM_LOSE;
	else:
		return ENUM_DRAW;

def runSimulation():
	trials = 100000;

	minPowerDiff = -5;
	maxPowerDiff = 5;

	powerDiff = minPowerDiff;
	while powerDiff <= maxPowerDiff:
		wins = 0;
		draws = 0;
		trial = 0;
		while trial < trials:
			result = doBattle(powerDiff);
			if result == ENUM_WIN:
				wins += 1;
			elif result == ENUM_DRAW:
				draws += 1;
			trial += 1;

		print str(powerDiff) + ": " + str(wins * 100.0 / trials) + "% win rate (" + str(draws * 100.0 / trials) + "% draw rate)";
		powerDiff += 1;


runSimulation();

