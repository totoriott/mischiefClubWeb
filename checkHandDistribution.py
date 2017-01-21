#!/usr/bin/env python
import random;
import pprint;
from operator import itemgetter;
import math;
import copy;

reversal card affects boost but not bet
different curves shapes for characters
knock lower bet to 5
remove card keep


deckTemplate = [
	# [copies, cheer, bet, isSpecial, name]

	[1, 5, -1, False, "Cheer ++++"],
	[1, 4, 0, False, "Cheer +++"],
	[1, 3, 1, False, "Cheer ++"],
	[2, 2, 2, False, "Cheer +/Bet+"],
	[1, 1, 3, False, "Bet ++"],
	[1, 0, 4, False, "Bet +++"],

	[0, -2, 0, True, "Cheer --"],

	[1, 0, 5, True, "Bet For All"],
	[1, 0, 0, True, "Reversal"],
];

''' in progress v2 deck
[8, 1, 1, False, "Bet/Cheer 1"],

[7, 2, 0, False, "Cheer 2"],
[6, 3, 0, False, "Cheer 3"],
[5, 4, -1, False, "Cheer 4"],
[2, 3, 0, True, "Cheer Solo"],

[7, 0, 2, False, "Bet 2"],
[5, -1, 3, False, "Bet 3"],
[2, 0, 3, True, "Bet Solo"],
[2, 0, 3, True, "Bet For All"],
[2, 0, 3, True, "Bet Balancer"],

[2, 0, 0, True, "Reversal"],
[1, 0, 0, True, "Underdog Boost"],
[1, 0, 0, True, "Mimic"],

[0, 2, 0, True, "Cheer Combo"], 

Avg. Cheer Cards: 3.3667
Avg. Bet Cards: 3.0022
Avg. Special Cards: 1.5603

Avg. Cheer: 7.3285
Avg. Bet: 5.7384

Avg. Positive Cheer: 7.9167
Avg. Positive Bet: 6.3425
'''


''' v1 deck
[7, 2, 0, False, "Cheer 2"],
[6, 3, 0, False, "Cheer 3"],
[5, 4, -1, False, "Cheer 4"],
[3, 5, -3, False, "Cheer 5"],
[4, 2, 0, True, "Cheer Combo"], 
[2, 3, 0, True, "Cheer Solo"],

[4, 1, 1, False, "Cheer/Bet 1"],
[4, 0, 2, False, "Bet 2"],
[3, -1, 3, False, "Bet 3"],
[2, -3, 4, False, "Bet 4"],
[2, 0, 3, True, "Bet Solo"],
[2, 0, 4, True, "Bet For All"],
[2, 0, 3, True, "Bet Balancer"],

[2, 0, 0, True, "Reversal"],
[1, 0, 0, True, "Underdog Boost"],
[1, 0, 0, True, "Mimic"],
Avg. Cheer Cards: 3.7029
Avg. Bet Cards: 2.3045
Avg. Special Cards: 1.9208

Avg. Cheer: 9.068
Avg. Bet: 4.2721

Avg. Positive Cheer: 10.1462
Avg. Positive Bet: 5.9406
'''

handSize = 6;

def getBuiltDeck():
	deck = [];
	for card in deckTemplate:
		count = 0;
		while count < card[0]:
			cardCopy = copy.deepcopy(card[1:]);
			deck.append(cardCopy);
			count += 1;
	return deck;

def getSpecialCardCount(hand):
	count = 0;
	for card in hand:
		if card[2] == True:
			count += 1;
	return count;

def getCheerCardCount(hand):
	count = 0;
	for card in hand:
		if card[0] > 0:
			count += 1;
	return count;

def getTotalCheer(hand):
	count = 0;
	for card in hand:
		count += card[0];
	return count;

def getTotalPositiveCheer(hand):
	count = 0;
	for card in hand:
		if card[0] > 0:
			count += card[0];
	return count;

def getBetCardCount(hand):
	count = 0;
	for card in hand:
		if card[1] > 0:
			count += 1;
	return count;

def getTotalBet(hand):
	count = 0;
	for card in hand:
		count += card[1];
	return count;

def getTotalPositiveBet(hand):
	count = 0;
	for card in hand:
		if card[1] > 0:
			count += card[1];
	return count;


def runSimulation():
	deck = getBuiltDeck();

	trials = 10000;

	totalSpecialCards = 0;
	totalCheerCards = 0;
	totalBetCards = 0;

	totalPositiveCheer = 0;
	totalPositiveBet = 0;

	totalCheer = 0;
	totalBet = 0;

	trial = 0;
	while trial < trials:
		random.shuffle(deck);
		hand = deck[:handSize];

		totalSpecialCards += getSpecialCardCount(hand);
		totalCheerCards += getCheerCardCount(hand);
		totalBetCards += getBetCardCount(hand);

		totalCheer += getTotalCheer(hand);
		totalBet += getTotalBet(hand);

		totalPositiveCheer += getTotalPositiveCheer(hand);
		totalPositiveBet += getTotalPositiveBet(hand);

		trial += 1;
	
	print str(len(deck)) + " cards in deck:";
	print "Example hands:";
	trial = 0;
	while trial < 5:
		random.shuffle(deck);
		hand = deck[:handSize];
		handNames = [x[3] for x in hand];
		print sorted(handNames);
		trial += 1;

	print "Avg. Cheer Cards: " + str(totalCheerCards * 1.0 / trials);
	print "Avg. Bet Cards: " + str(totalBetCards * 1.0 / trials);
	print "Avg. Special Cards: " + str(totalSpecialCards * 1.0 / trials);
	print;
	print "Avg. Cheer: " + str(totalCheer * 1.0 / trials);
	print "Avg. Bet: " + str(totalBet * 1.0 / trials);
	print;
	print "Avg. Positive Cheer: " + str(totalPositiveCheer * 1.0 / trials);
	print "Avg. Positive Bet: " + str(totalPositiveBet * 1.0 / trials);


runSimulation();

