from django.http import HttpResponse
from copy import deepcopy

import random;
from tablesaltGame.models import *
from tablesaltGame.aiModels import *

def createDeckIDArrayFromTemplates(boostCardTemplates, singularCopyOfCard):
	boostDeck = [];
	for template in boostCardTemplates:
		if template.enabled:
			copies = 0;

			copiesOfCard = 1;
			if (singularCopyOfCard == False):
				copiesOfCard = template.copiesOfCard;

			while copies < copiesOfCard:
				boostDeck.append(template.id);

				copies += 1;

	random.shuffle(boostDeck)
	return boostDeck;	

def createGameWithConfigs(gameConfiguration, competitorDeckTemplate, boostDeckTemplate, playerNames, isPublic):
	competitorDeck = createDeckIDArrayFromTemplates(competitorDeckTemplate, True);
	boostDeck = createDeckIDArrayFromTemplates(boostDeckTemplate, False);

	# TODO: maybe move and unmove deserializing players
	players = len(playerNames); # these should be escaped passed in or else things are Very Bad
	curPlayer = 0;
	serializedPlayerArray = [];
	while curPlayer < players:
		gamePlayer = GamePlayer();
		gamePlayer.initWithId(curPlayer, playerNames[curPlayer]);
		if (playerNames[curPlayer] == "[AI-ROBOT]"): #TODO: remove hack
			aiClass = DefaultAiModel(None, 0);
			newAi = [0, "AI"]; # TODO - AI again aiClass.getRandomAiModelWithName();

			gamePlayer.aiModel = newAi[0];
			gamePlayer.playerName = newAi[1];
			gamePlayer.passcode = "0000";
		serializedPlayerArray.append(str(gamePlayer.serializeToString()));
		curPlayer += 1;	

	newGame = GameData(competitorCardDeck=competitorDeck, boostCardDeck=boostDeck, serializedPlayers=serializedPlayerArray, discardPile=[],
		 public=isPublic, configurationId=gameConfiguration.id);
	newGame.save();
	
	return newGame;

def createANewGame(request, playerNames, isPublic):
	playerCount = len(playerNames);
	allGameConfigurations = GameConfiguration.objects.filter(enabled=True, numberOfPlayers=playerCount);
	if (len(allGameConfigurations) != 1):
		return HttpResponse("Make sure exactly one game configuration is enabled!")
	if (len(playerNames) != playerCount):
		return HttpResponse("Number of player names doesn't equal player count!")
	
	newGame = createGameWithConfigs(allGameConfigurations[0], CompetitorCard.objects.filter(enabled=True), BoostCard.objects.filter(enabled=True), playerNames, isPublic);

	return newGame.id; # TODO: error checking