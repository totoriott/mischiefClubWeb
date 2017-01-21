#!/usr/bin/env python
import random;
import pprint;
from operator import itemgetter;
import math;
import copy;

characterNames = ["Waka", "Mr. Caramel", "MASAMUNE", "Sohaya", "Chrysoberyl", "Fantastic Melty Core", "Repentor(cross)", "Sakakibara Tatsumaru", "Trench", "Seven", "Zentheil", "Ritornello", "Remiel", "Vektrakt", "Veridia", "Niventia", "Rose Alice", "Acedia", "Sophie Anders S"];

# =============================================

#abilityBoostDeck = [0, 1, 1, 2, 2, 3, 3, 4, 4, 5];
#abilityBoostDeck = [0, 1, 2, 3, 4, 5];
#abilityBoostDeck = [0, 0, 0];
abilityBoostDeck = [-1, 0.5, 0, 1, 2, 4];

def getPowerFromCheerAndCheckpoints(cheer, checkpoints):
	curPower = 0;
	for checkpoint in checkpoints:
		if cheer >= checkpoint[1]:
			curPower = checkpoint[0];
	return curPower;

def getWinPercentageVersusDeck(character, deck, trials=1000):
	wins = 0;

	trial = 0;
	while trial < trials:
		random.shuffle(deck);
		otherChara1 = deck[0];
		otherChara2 = deck[1];

		if (character[1] != otherChara1[1] and character[1] != otherChara2[1]):
			# do a fight
			cheer = math.floor(random.normalvariate(12, 6));
			while cheer < 0 or cheer > 32:
				cheer = random.normalvariate(12, 6);

			# break cheer into 3 points
			cheerPoint1 = math.floor(random.random() * (cheer+1));
			cheerPoint2 = math.floor(random.random() * (cheer+1));
			if (cheerPoint2 < cheerPoint1):
				tmp = cheerPoint1;
				cheerPoint1 = cheerPoint2;
				cheerPoint2 = tmp;

			playerCheer = [cheerPoint1, cheerPoint2, cheer - cheerPoint2];
			random.shuffle(playerCheer);
			p1cheer = playerCheer[0];
			p2cheer = playerCheer[1];
			p3cheer = playerCheer[2];

			chara1checkpoints = character[2:];
			chara2checkpoints = otherChara1[2:];
			chara3checkpoints = otherChara2[2:];

			p1power = getPowerFromCheerAndCheckpoints(p1cheer, chara1checkpoints);
			p2power = getPowerFromCheerAndCheckpoints(p2cheer, chara2checkpoints);
			p3power = getPowerFromCheerAndCheckpoints(p3cheer, chara3checkpoints);

			random.shuffle(abilityBoostDeck);
			# ability, then cheer, then randomizer card as tiebreaker
			p1power += abilityBoostDeck[0] * 1.00001 + p1cheer / 100.0;
			p2power += abilityBoostDeck[1] * 1.00001 + p2cheer / 100.0;
			p3power += abilityBoostDeck[2] * 1.00001 + p3cheer / 100.0;
			if (p1power > p2power and p1power > p3power):
				wins += 1; 

			trial += 1;

	#print character[1] + " vs. deck: " + str(wins * 100.0 / trials) + "% win rate";
	return wins * 1.0 / trials

# =============================================

def generateCharaList():
	# assume a 5-ability random deviation in max power is possible 
	# [power 0, 1, 2, 3, 4, 5];

	# minPowerSpread = [5, 8, 7, 0, 0, 0]
	# maxPowerSpread = [0, 0, 0, 7, 7, 6]

	minPowerSpread = [6, 7, 6, 0, 0, 0, 0]
	maxPowerSpread = [0, 0, 0, 0, 13, 7, 0]
	curveMinAtPowerLevel = [0, 0, 0, 4, 6, 8, 10] # if your max power is X, your min cheer is Y
	curveMaxAtPowerLevel = [0, 0, 0, 7, 8, 10, 12] # if your max power is X, your max cheer is Y

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
					if (curCheer > curveMaxAtPowerLevel[charaMaxPower]): 
						invalidCheckpoints = True; 
					character.append([checkpoint, curCheer]);

					curCheer += math.ceil(1 + (random.random() * 4.0));

				if character[-1][1] < curveMinAtPowerLevel[charaMaxPower] and len(character) >= 5: # let's say you have to get some cheer tho (this checks the last checkpoint)
					invalidCheckpoints = True; 

			if invalidChara == False:
				characters.append(character);

	return sorted(characters, key=itemgetter(0), reverse=True);

def getGoodCharaList():
	goodList = False;

	charaWinRates = [];
	characters = [];

	while goodList == False:
		characters = generateCharaList();

		goodList = True;

		for character in characters:
			if len(character) < 5: # power rating, name, [# checkpoints]
				goodList = False; # less than 3 checkpoints	

				if len(character) > 7: # power rating, name, [# checkpoints]
					goodList = False; # more than 5 checkpoints	

		charaWinRates = [];
		if goodList:
			# sort by overall win rate
			i = 0;
			while i < len(characters):
				chara = characters[i];
				charaWinRates.append([getWinPercentageVersusDeck(chara, copy.deepcopy(characters)) * 100.0, chara])
				i += 1;

			charaWinRates = sorted(charaWinRates, key=itemgetter(0), reverse=True);
			if (charaWinRates[0][0] >= 50.0):
				print "Rejecting best win " + str(charaWinRates[0][0]);
				#if (charaWinRates[0][0] <= 45.0):
				#	pp = pprint.PrettyPrinter(indent=2);
				#	pp.pprint(charaWinRates);
				goodList = False;

			if (charaWinRates[-1][0] <= 25.0 and goodList):
				print "Rejecting worst win " + str(charaWinRates[-1][0]);
				#if (charaWinRates[0][0] <= 45.0):
				#	pp = pprint.PrettyPrinter(indent=2);
				#	pp.pprint(charaWinRates);
				goodList = False;

	pp = pprint.PrettyPrinter(indent=2);
	pp.pprint(charaWinRates);

def testGoodCharaList(goodCharaList):
	charaList = [];
	charaWinRates = [];
	for chara in goodCharaList:
		charaList.append(chara[1:][0]);

	i = 0;
	while i < len(charaList):
		chara = charaList[i];
		charaWinRates.append([getWinPercentageVersusDeck(chara, copy.deepcopy(charaList), 20000) * 100.0, chara])
		i += 1;

	charaWinRates = sorted(charaWinRates, key=itemgetter(0), reverse=True);
	pp = pprint.PrettyPrinter(indent=2);
	pp.pprint(charaWinRates);

#getGoodCharaList();

goodCharaList = [ [40.785, [1.5, 'Chrysoberyl', [2, 0], [3, 4.0], [4, 7.0]]],
  [39.205, [3.5, 'MASAMUNE', [2, 0], [3, 5.0], [4, 7.0]]],
  [38.565, [2.5, 'Repentor', [4, 0], [2, 3.0], [1, 5.0], [3, 8.0]]],
  [ 37.62,
    [3.0, 'Fantastic Melty Core', [1, 0], [2, 2.0], [4, 7.0], [5, 10.0]]],
  [ 37.355,
    [ 2.5,
      'Sakakibara Tatsumaru',
      [1, 0],
      [2, 3.0],
      [3, 5.0],
      [4, 8.0],
      [5, 10.0]]],
  [36.0, [2.0, 'Vektrakt', [2, 0], [4, 5.0], [3, 7.0]]],
  [35.97, [1.5, 'Eagle', [2, 0], [1, 3.0], [3, 7.0], [5, 9.0]]],
  [35.23, [3.5, 'Ritornello', [3, 0], [1, 2.0], [2, 6.0], [4, 8.0]]],
  [34.5, [2.0, 'Trench', [1, 0], [3, 3], [2, 6.0], [4, 9.0]]],
  [32.175, [3.5, 'Niventia', [1, 0], [2, 4.0], [3, 7.0], [4, 9.0]]],
  [31.385, [2.5, 'Seven', [1, 0], [3, 3.0], [4, 6.0], [2, 8.0]]],
  [30.740000000000002, [2.0, 'Waka', [3, 0], [2, 4.0], [1, 7.0]]],
  [ 30.264999999999997,
    [2.5, 'Sophie Anders S', [0, 0], [1, 2.0], [2, 5.0], [3, 8.0], [5, 10.0]]],
  [29.985, [2.0, 'Remiel', [1, 0], [2, 3.0], [3, 6.0]]],
  [28.46, [1.5, 'Acedia', [1, 0], [2, 2.0], [4, 4.0], [0, 8.0]]],
  [28.16, [2.0, 'Veridia', [2, 0], [4, 4.0], [1, 6.0]]],
  [27.355, [3.5, 'Mr. Caramel', [0, 0], [2, 2.0], [1, 4.0], [3, 6.0]]],
  [27.139999999999997, [2.0, 'Zentheil', [1, 0], [3, 3.0], [2, 6.0]]]];
  
testGoodCharaList(goodCharaList);

'''
v3 chara list
[ [44.7, [3.5, 'Waka', [2, 0], [3, 2.0], [4, 5.0], [5, 10.0]]],
  [44.7, [3.5, 'Vektrakt', [2, 0], [4, 5.0], [5, 8.0]]],
  [40.6, [3.5, 'Mr. Caramel', [2, 0], [4, 5.0], [5, 9.0]]],
  [40.400000000000006, [3.0, 'Repentor(cross)', [2, 0], [3, 3.0], [4, 8.0]]],
  [38.7, [3.5, 'Ritornello', [2, 0], [3, 5.0], [4, 7.0], [5, 9.0]]],
  [38.7, [3.0, 'Sakakibara Tatsumaru', [2, 0], [3, 3.0], [4, 7.0]]],
  [36.1, [2.5, 'Niventia', [1, 0], [2, 2.0], [3, 4.0], [4, 8.0]]],
  [34.599999999999994, [2.5, 'Sohaya', [1, 0], [2, 3.0], [3, 5.0], [4, 7.0]]],
  [32.1, [1.5, 'Rose Alice', [0, 0], [2, 2.0], [3, 5.0]]],
  [31.6, [2.5, 'Sophie Anders S', [1, 0], [2, 3.0], [3, 5.0], [4, 8.0]]],
  [30.8, [2.0, 'Acedia', [1, 0], [2, 2.0], [3, 6.0]]],
  [30.599999999999998, [2.0, 'Remiel', [0, 0], [1, 2.0], [3, 4.0], [4, 8.0]]],
  [28.9, [2.0, 'Fantastic Melty Core', [1, 0], [2, 3.0], [3, 6.0]]],
  [ 28.499999999999996,
    [2.0, 'Veridia', [0, 0], [1, 2.0], [2, 4.0], [3, 6.0], [4, 8.0]]],
  [ 27.400000000000002,
    [2.5, 'MASAMUNE', [0, 0], [1, 3.0], [2, 6.0], [3, 8.0], [5, 10.0]]],
  [ 27.400000000000002,
    [1.5, 'Zentheil', [0, 0], [1, 2.0], [2, 4.0], [3, 7.0]]],
  [27.3, [1.5, 'Trench', [0, 0], [1, 2.0], [2, 4.0], [3, 6.0]]],
  [26.900000000000002, [2.0, 'Seven', [1, 0], [2, 4.0], [3, 7.0]]],
  [25.900000000000002, [2.0, 'Chrysoberyl', [1, 0], [2, 3.0], [3, 7.0]]]]

v2 chara list
[ [49.0, [4.5, 'MASAMUNE', [3, 0], [4, 5.0], [6, 10.0]]],
  [43.1, [3.5, 'Mr. Caramel', [2, 0], [4, 5.0], [5, 8.0]]],
  [41.4, [3.0, 'Zentheil', [2, 0], [3, 1.0], [4, 6.0]]],
  [40.2, [3.5, 'Sohaya', [2, 0], [3, 4.0], [4, 8.0], [5, 10.0]]],
  [39.900000000000006, [3.0, 'Vektrakt', [2, 0], [3, 2.0], [4, 6.0]]],
  [38.7, [3.0, 'Rose Alice', [2, 0], [3, 4.0], [4, 8.0]]],
  [38.4, [3.5, 'Trench', [2, 0], [3, 4.0], [5, 9.0]]],
  [ 37.0,
    [3.0, 'Sophie Anders S', [1, 0], [2, 2.0], [3, 4.0], [4, 6.0], [5, 9.0]]],
  [34.0, [2.5, 'Veridia', [1, 0], [3, 3.0], [4, 8.0]]],
  [ 30.599999999999998,
    [2.0, 'Fantastic Melty Core', [1, 0], [2, 2.0], [3, 5.0]]],
  [29.099999999999998, [2.0, 'Seven', [1, 0], [2, 1.0], [3, 4.0]]],
  [28.9, [2.5, 'Ritornello', [1, 0], [3, 4.0], [4, 8.0]]],
  [27.700000000000003, [1.5, 'Waka', [0, 0], [2, 1.0], [3, 6.0]]],
  [ 27.6,
    [2.0, 'Repentor(cross)', [0, 0], [1, 1.0], [2, 4.0], [3, 6.0], [4, 7.0]]],
  [ 27.400000000000002,
    [2.0, 'Chrysoberyl', [0, 0], [2, 3.0], [3, 7.0], [4, 8.0]]],
  [27.3, [2.0, 'Acedia', [1, 0], [2, 4.0], [3, 5.0]]],
  [27.0, [1.5, 'Sakakibara Tatsumaru', [0, 0], [1, 1.0], [2, 3.0], [3, 7.0]]],
  [ 26.900000000000002,
    [3.0, 'Niventia', [0, 0], [2, 5.0], [3, 8.0], [4, 9.0], [6, 10.0]]],
  [26.1, [2.0, 'Remiel', [1, 0], [2, 3.0], [3, 4.0]]]]
'''

''' v1 chara list
[ [49.4, [4.0, 'Niventia', [3, 0], [4, 8.0], [5, 15.0]]],
  [ 46.400000000000006,
    [3.5, 'Ritornello', [1, 0], [3, 4.0], [4, 11.0], [5, 18.0], [6, 21.0]]],
  [44.6, [3.5, 'MASAMUNE', [2, 0], [3, 5.0], [5, 13.0]]],
  [42.4, [3.0, 'Sohaya', [1, 0], [2, 4.0], [5, 12.0]]],
  [40.699999999999996, [3.0, 'Mr. Caramel', [2, 0], [3, 5.0], [4, 13.0]]],
  [37.7, [3.0, 'Fantastic Melty Core', [2, 0], [3, 6.0], [4, 14.0]]],
  [36.7, [3.0, 'Repentor(cross)', [0, 0], [1, 4.0], [3, 8.0], [4, 12.0], [6, 19.0]]],
  [35.6, [3.0, 'Sakikibara Tatsumaru', [2, 0], [3, 7.0], [4, 15.0]]],
  [34.8, [3.0, 'Acedia', [2, 0], [3, 7.0], [4, 14.0]]],
  [34.8, [3.0, 'Seven', [2, 0], [3, 5.0], [4, 13.0]]],
  [34.4, [3.0, 'Zentheil', [1, 0], [2, 7.0], [4, 13.0], [5, 16.0]]],
  [30.7, [2.5, 'Vektrakt', [1, 0], [2, 5.0], [4, 13.0]]],
  [25.2, [2.0, 'Remiel', [1, 0], [2, 5.0], [3, 12.0]]],
  [24.7, [2.0, 'Veridia', [1, 0], [2, 8.0], [3, 12.0]]],
  [ 23.0,
    [ 2.0,
      'Sophie Anders S',
      [0, 0], [1, 3.0], [2, 11.0], [3, 16.0], [4, 22.0]]],
  [22.8, [1.5, 'Chrysoberyl', [0, 0], [1, 5.0], [2, 9.0], [3, 17.0]]],
  [22.3, [2.0, 'Rose Alice', [1, 0], [2, 8.0], [3, 15.0]]],
  [21.3, [1.5, 'Trench', [0, 0], [1, 7.0], [2, 12.0], [3, 15.0]]],
  [ 20.8,
    [1.5, 'Waka', [0, 0], [1, 5.0], [2, 11.0], [3, 15.0]]]]'''