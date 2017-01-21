import random;
import math;
from tablesaltGame.models import *;

# Default AI - usually supports early then will play mostly on that one. Pretty naive
# ID 0.
class DefaultAiModel:
	def getRandomAiModelWithName(this):
		return [0, "AI"]; # TODO

	gameManager = None;
	playerID = -1;

	def __init__(this, myGameManager, playerNumber):
		this.gameManager = myGameManager;
		this.playerID = playerNumber;

	def getChosenPlayCard(this):
		thisPlayer = this.gameManager.players[this.playerID];
		currentMatch = this.gameManager.getCurrentMatch();

		supportedID = -1; # if you've backed someone, know it
		for actionTuple in currentMatch.playerPerformedActions[this.playerID]: 
			if actionTuple[0] == 17:
				supportedID = actionTuple[1];

		actionTuple = {};

		# picks a random card
		cardPicked = int(math.floor(random.random() * (len(thisPlayer.hand))));

		actionTuple["optionCard"] = cardPicked;
		actionTuple["optionTarget"] = int(math.floor(random.random() * (len(this.gameManager.matches[-1].competitors))));

		# TODO: make sure to pick proper supporter

		actionTuple["playerDataVersion"] = thisPlayer.playerDataVersion;

		return actionTuple;

	def getChosenDraftCard(this):
		thisPlayer = this.gameManager.players[this.playerID];
		currentMatch = this.gameManager.getCurrentMatch();

		# TODO: yea we just don't draft anything for now
		actionTuple = {};
		actionTuple["optionAddCard"] = 100;
		actionTuple["optionRemoveCard"] = 100;

		actionTuple["playerDataVersion"] = thisPlayer.playerDataVersion;
		return actionTuple;