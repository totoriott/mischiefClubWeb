#!/usr/bin/env python
import random;
import pprint;
from operator import itemgetter;
import math;

characterNames = ["Waka", "Mr. Caramel", "MASAMUNE", "Sohaya", "Chrysoberyl", "Fantastic Melty Core", "Repentor(cross)", "Sakakibara Tatsumaru", "Trench", "Seven", "Zentheil", "Ritornello", "Remiel", "Vektrakt", "Veridia", "Niventia", "Rose Alice", "Acedia", "Sophie Anders S"];

# =============================================

abilityBoostDeck = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5];

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

def getPowerFromCheerAndCheckpoints(cheer, checkpoints):
	curPower = 0;
	for checkpoint in checkpoints:
		if cheer >= checkpoint[1]:
			curPower = checkpoint[0];
	return curPower;

def getWinPercentageVersusCharacter(character, character2):
	trials = 1000;

	# TODO: fair power spread
	chara1checkpoints = character[2:];
	chara2checkpoints = character2[2:];

	wins = 0;
	trial = 0;
	while trial < trials:
		# TODO: this
		cheer = 8 + math.floor(random.random() * 41);

		p1cheer = cheer - math.floor(random.random() * (cheer+1));
		p2cheer = cheer - p1cheer;

		p1power = getPowerFromCheerAndCheckpoints(p1cheer, chara1checkpoints);
		p2power = getPowerFromCheerAndCheckpoints(p2cheer, chara2checkpoints);

		powerDiff = p1power - p2power; 

		if doBattle(powerDiff) == ENUM_WIN:
			wins += 1;
		trial += 1;

	if abs(50 - (wins * 100.0 / trials)) > 30:
		print "  WARNING: " + character[1] + " vs. " + character2[1] + ": " + str(wins * 100.0 / trials) + "% win rate";
	# print character[1] + " vs. " + character2[1] + ": " + str(wins * 100.0 / trials) + "% win rate";
	return wins * 1.0 / trials;

def getWinPercentageVersusDeck(character, deck):
	charasFought = 0;
	totalWinPercent = 0;

	for otherChara in deck:
		if character[1] != otherChara[1]: # if the names are the same, ignore
			totalWinPercent += getWinPercentageVersusCharacter(character, otherChara);
			charasFought += 1;

	#print character[1] + " vs. deck: " + str(totalWinPercent * 100.0 / charasFought) + "% win rate";
	return totalWinPercent * 1.0 / charasFought

# =============================================

def generateCharaList():
	# assume a 5-ability random deviation in max power is possible 
	# [power 0, 1, 2, 3, 4, 5];
	minPowerSpread = [7, 7, 6, 0, 0, 0]
	maxPowerSpread = [0, 0, 2, 7, 6, 5]

	minPowers = [];
	power = 0;
	while power < len(minPowerSpread):
		count = 0;
		while (count < minPowerSpread[power]):
			minPowers.append(power);
			count += 1;
		power += 1;

	maxPowers = [];
	power = 0;
	while power < len(maxPowerSpread):
		count = 0;
		while (count < maxPowerSpread[power]):
			maxPowers.append(power);
			count += 1;
		power += 1;

	random.shuffle(minPowers);
	random.shuffle(maxPowers);
	characters = [];

	for chara in characterNames:
		charaId = len(characters);
		invalidChara = True;

		while invalidChara:
			charaMinPower = minPowers[charaId];
			charaMaxPower = maxPowers[charaId];

			powerRating = (charaMinPower + charaMaxPower) / 2.0;
			character = [powerRating, chara];
			invalidChara = False;

			# create the Cheer checkpoints
			charaPowerCheckpoints = [charaMinPower];
			curPower = charaMinPower;
			curPower += 1;
			while curPower < charaMaxPower:
				if random.random() < 0.75: # probably checkpoint at every power, but not necessarily
					charaPowerCheckpoints.append(curPower);
				curPower += 1;	
			charaPowerCheckpoints.append(curPower);

			invalidCheckpoints = True;
			while invalidCheckpoints:
				character = character[:2];
				invalidCheckpoints = False;

				curCheer = 0;
				for checkpoint in charaPowerCheckpoints:
					if (curCheer >= 20): #let's say you can't get more than 20 cheer
						invalidCheckpoints = True; 
					character.append([checkpoint, curCheer]);

					curCheer += math.ceil(2 + (random.random() * 6.0));

				if character[-1][1] < 12 and len(character) >= 5: # let's say you have to get some cheer tho (this checks the last checkpoint)
					invalidCheckpoints = True; 

			if invalidChara == False:
				characters.append(character);

	return sorted(characters, key=itemgetter(0), reverse=True);

def getGoodCharaList():
	goodList = False;

	charaWinRates = [];

	while goodList == False:
		characters = generateCharaList();

		goodList = True;

		for character in characters:
			if len(character) < 5: # power rating, name, [# checkpoints]
				goodList = False; # less than 3 checkpoints	

	# sort by overall win rate
	for chara in characters:
		charaWinRates.append(getWinPercentageVersusDeck(chara, characters) * 100.0);
	i = 0;
	while i < len(charaWinRates):
		characters[i].insert(0, charaWinRates[i]);
		i += 1;

	return sorted(characters, key=itemgetter(0), reverse=True);

characters = getGoodCharaList();

pp = pprint.PrettyPrinter(indent=2);
pp.pprint(characters);