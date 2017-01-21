#!/usr/bin/env python
import random;
import pprint;
from operator import itemgetter;
import math;
import copy;

deckTemplate = [
	# [copies, cheer, bet, isSpecial, name]
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
];

playerCount = 4;
handSize = 6;
betModifiersFromDrop = [20, 17, 15, 12];

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

class TestPlayer:
	# TODO: play on different characters
	def __init__(this):
		this.hand = [];
		this.played = [];
		this.inMatch = True;
		this.betModifier = 0; # how much bet is modified from when they dropped

	def resetMatchStatus(this):
		this.played = [];
		this.inMatch = True;
		this.betModifier = 0;

	def __repr__(this):
		string = "Hand: ";
		for card in this.hand:
			string += card[3] + ", ";
		string = string[:-1];

		string += " || Played: ";
		for card in this.played:
			string += card[3] + ", "
		string = string[:-1];

		string += " || Bet Modifier: " + str(this.betModifier);

		return string;

def countOfPlayersStillInMatch(players):
	count = 0;
	for player in players:
		if player.inMatch:
			count += 1;
	return count;

def runSimulation():
	pp = pprint.PrettyPrinter(indent=2)
	deck = getBuiltDeck();

	trials = 1;

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

		# create player hands
		players = []
		pCount = 0;
		while pCount < playerCount:
			newPlayer = TestPlayer();
			newPlayer.hand = deck[pCount*handSize : (pCount+1)*handSize];
			players.append(newPlayer);

			pCount += 1;

		# do match
		dropoutPlayersInOrder = [];
		while countOfPlayersStillInMatch(players) > 0: # play a round
			playersDroppedThisRound = [];

			for player in players:
				if player.inMatch:
					if len(player.hand) == 0 or countOfPlayersStillInMatch(players) == 1: # must drop
						player.inMatch = False;
						playersDroppedThisRound.append(player);
					else:
						playedCard = player.hand.pop();
						player.played.append(playedCard);

						if random.random() < 0.25: # TODO: decide when to drop
							player.inMatch = False;
							playersDroppedThisRound.append(player);

			if len(playersDroppedThisRound) > 0:
				dropoutPlayersInOrder.append(playersDroppedThisRound);

		currentDropoutLevel = 0;
		for dropoutGroup in dropoutPlayersInOrder:
			nextDropoutLevel = currentDropoutLevel;

			for player in dropoutGroup:
				player.betModifier = betModifiersFromDrop[currentDropoutLevel];
				nextDropoutLevel += 1;

			currentDropoutLevel = nextDropoutLevel;

		pp.pprint(players);
		# TODO: sim, work in betModifiersFromDrop

		trial += 1;
	

runSimulation();

