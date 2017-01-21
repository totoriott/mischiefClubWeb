from django.db import models
from ast import literal_eval;
from django.utils.safestring import mark_safe
from django.utils import timezone;
from HTMLParser import HTMLParser  # py2
from django.conf import settings

import time

class AbilityEnum:
	ABILITY_NONE = 0;
	ABILITY_UNUSED = 1;
	ABILITY_CHEER_COLLAB = 2;
	ABILITY_CHEER_SOLO = 3;
	ABILITY_BET_SOLO = 4;
	ABILITY_BET_BOOST = 5;
	ABILITY_BET_BALANCE = 6; # DEPRECATED
	ABILITY_REVERSAL = 7;
	ABILITY_UNDERDOG = 8;
	ABILITY_MIMIC = 9;
	ABILITY_SUPPORTER = 10; 
	ABILITY_FREE_POINTS = 11; 
	ABILITY_INVERTER = 12; 
	ABILITY_PLAY_FACE_UP = 13;
	ABILITY_SOLO_STAR = 14;
	ABILITY_BACKUP_PLAN = 15;
	ABILITY_NULLIFY_IF_NOT_ONLY_CARD = 16;

	TYPE_ENUMS = (
		(ABILITY_NONE, "None"),
		(ABILITY_CHEER_COLLAB, "Cheer Collab"),
		(ABILITY_CHEER_SOLO, "Cheer Solo"),
		(ABILITY_BET_SOLO, "Bet Solo"),
		(ABILITY_BET_BOOST, "Bet Boost"),
		(ABILITY_BET_BALANCE, "DEPRECATED - Bet Balance"),
		(ABILITY_REVERSAL, "Reversal"),
		(ABILITY_UNDERDOG, "Underdog"),
		(ABILITY_MIMIC, "Mimic"),
		(ABILITY_SUPPORTER, "Supporter"),
		(ABILITY_FREE_POINTS, "Free Points"),
		(ABILITY_INVERTER, "Inverter"),
		(ABILITY_PLAY_FACE_UP, "Play Face Up"),
		(ABILITY_SOLO_STAR, "Solo Star"),
		(ABILITY_BACKUP_PLAN, "Backup Plan"),
		(ABILITY_NULLIFY_IF_NOT_ONLY_CARD, "Nullify if Not Only Card"),
	);

class CompetitorCard(models.Model):
	name = models.CharField(max_length=200);
	shortName = models.CharField(max_length=20);

	textDescription = models.CharField(max_length=500, default="no description");

	cheerTrackValues = models.CharField(max_length=500);

	enabled = models.BooleanField(default=True);

	# this mostly exists to let you confirm you setup the character properly
	def abilityRangeString(this):
		cheerTrackValueArray = literal_eval(this.cheerTrackValues);
		return str(cheerTrackValueArray[0][0]) + " - " + str(cheerTrackValueArray[-1][0]);

	def __str__(this):
		return "CC-" + this.name;

	def getAbilityWithCheerValue(this, cheer):
		cheerTrackValueArray = literal_eval(this.cheerTrackValues);
		if cheer <= 0:
			cheer = 0;

		ability = 0;

		for cheerTuple in cheerTrackValueArray:
			if cheer >= cheerTuple[1]:
				ability = cheerTuple[0];

		return int(ability);

	def getIndexOfHighestCheerTier(this, cheer):
		cheerTrackValueArray = literal_eval(this.cheerTrackValues);
		highestTier = 0;

		index = 0;
		for cheerTuple in cheerTrackValueArray:
			if cheer >= cheerTuple[1]:
				highestTier = index;
			index += 1;

		return highestTier;	

	def getRulesCardHTML(this, opacity=1):
		cardId = this.id;

		cardURL = settings.STATIC_URL + "/competitorcards/" + str(cardId) + ".png";
		imgWidth = 96;

		return '<img src="'+cardURL+'" width="'+str(imgWidth)+'" style="opacity:'+str(opacity)+'"/><!--'+this.name+'-->'; # TODO

class BoostCard(models.Model):
	name = models.CharField(max_length=200);
	textDescription = models.CharField(max_length=500, default="no description");
	
	abilityType = models.IntegerField(default=AbilityEnum.ABILITY_NONE, choices=AbilityEnum.TYPE_ENUMS); 

	cheerAmount = models.IntegerField(default=0);
	betAmount = models.IntegerField(default=0);

	enabled = models.BooleanField(default=True);
	advancedCard = models.BooleanField(default=False);
	copiesOfCard = models.IntegerField(default=1);

	def __str__(this):
		return "BC-" + this.name;

	def getPlayedCardHTML(this, playerId=0):
		return this.getCardHTML(playerId, 64);

	def getRulesCardHTML(this, playerId=0):
		return this.getCardHTML(playerId, 96);

	def getCardHTML(this, playerId, imgWidth):
		cardId = this.id;

		cardURL = settings.STATIC_URL + "/boostcards/" + str(cardId) + "_p" + str(playerId) + ".png";

		tooltip = this.name + "&#13;" + this.textDescription;

		return '<img src="'+cardURL+'" width="'+str(imgWidth)+'" title="'+tooltip+'"/>';

	def getBackCardHTML(this, playerId):
		cardId = "back";
		imgWidth = 64;
		cardURL = settings.STATIC_URL + "/boostcards/" + str(cardId) + "_p" + str(playerId) + ".png";

		return '<img src="'+cardURL+'" width="'+str(imgWidth)+'" title=""/>';

	def getHelperDescription(this):
		desc = this.name + "<br>";
		desc += this.textDescription.replace("&#13;","<br>");
		return desc;

class GameConfiguration(models.Model):
	name = models.CharField(max_length=200);

	numberOfMatches = models.IntegerField(default=5); 
	charactersPerMatch = models.IntegerField(default=3); # TODO: deprecated
	numberOfPlayers = models.IntegerField(default=4);  

	handSize = models.IntegerField(default=6); # TODO: deprecated - we give full deck now
	discardDownHandSizeAfterMatch = models.IntegerField(default=3); # TODO: can remove

	betTrackValues = models.CharField(max_length=500); # TODO: deprecated
	randomizerValues = models.CharField(max_length=500); 

	enabled = models.BooleanField(default=True);

class GameData(models.Model):
	DEFAULT_PASSCODE = "0000";

	public = models.BooleanField(default=False);
	creationTime = models.DateTimeField(default=timezone.now);
	passcode = models.CharField(max_length=10000, default="");

	notes = models.CharField(max_length=1000, default="", blank=True); # notes for data collection use

	configurationId = models.IntegerField(default=1);

	competitorCardDeck = models.CharField(max_length=1000); # actually a CommaSeparatedIntegerField, but validating that is bad
	boostCardDeck = models.CharField(max_length=1000); # actually a CommaSeparatedIntegerField, but validating that is bad
	discardPile = models.CharField(max_length=1000); # actually a CommaSeparatedIntegerField, but validating that is bad # TODO: can remove

	serializedPlayers = models.CharField(max_length=10000);
	serializedMatches = models.CharField(max_length=10000);

	dataVersion = models.IntegerField(default=0); # used for validation of player actions

	def isGamePasscoded(self):
		return len(self.passcode) > 0 and self.passcode != self.DEFAULT_PASSCODE;
		
	def isGameDataPlayable(self):
		return self.public and timezone.now() >= self.creationTime; # TODO: make non-public games playable

	def numberOfHumanPlayers(this):
		players = this.deserializePlayers();
		humans = 0;

		for player in players:
			if player.aiModel < 0:
				humans += 1;

		return humans;

	def isGameNotOver(this):
		matches = this.deserializeMatches();
		if len(matches) == 5 and matches[-1].matchResolved: # TODO: don't hardcode match count
			return False; 

		return True;

	def isGameEmpty(this):
		players = this.deserializePlayers();

		for player in players:
			if len(player.passcode) != 0:
				return False;

		return True;

	def deserializePlayers(this):
		players = [];

		playersArray = literal_eval(this.serializedPlayers);

		for serializedPlayer in playersArray:
			newPlayer = GamePlayer();
			newPlayer.deserializeFromString(serializedPlayer);
			players.append(newPlayer);

		return players;
		
	def serializeAndSetPlayers(this, players):
		sPlayers = [];
		for thisPlayer in players:
			sPlayers.append(str(thisPlayer.serializeToString()));
			
		this.serializedPlayers = sPlayers;

	def serializeAndSetMatches(this, matches):
		sMatches = [];
		for thisMatch in matches:
			sMatches.append(str(thisMatch.serializeToString()));
			
		this.serializedMatches = sMatches;

	def deserializeMatches(this):
		if len(this.serializedMatches) == 0:
			return [];

		matches = [];

		matchesArray = literal_eval(this.serializedMatches);

		for serializedMatch in matchesArray:
			newMatch = GameMatch();
			newMatch.deserializeFromString(serializedMatch);
			matches.append(newMatch);

		return matches;

	def gameListString(this): # how the game is represented in public lobbies
		if (this.isGameNotOver() == False):
			return "#" + str(this.id) +  ": Game finished";
		else:
			matches = this.deserializeMatches();
			if len(matches) == 0:
				return "#" + str(this.id) +  ": New game";
			else:
				return "#" + str(this.id) +  ": Match #" + str(len(matches));
		
	def playerJoinButtonTuples(this): # the buttons returned to the lobby.py
		players = this.deserializePlayers();

		playerButtons = [];
		for player in players:
			pString = "(P" + str(player.playerId+1) + ") ";
			if (player.aiModel >= 0):
				pString = "(AI) "
			
			unescape = HTMLParser().unescape
			cannotEnterAsThisPlayer = False; #player.aiModel >= 0
			#TODO: unescape name
			buttonTuple = [pString + str(player.playerName), str(this.id)+","+str(player.playerId+1), cannotEnterAsThisPlayer];
			playerButtons.append(buttonTuple);
			
		return playerButtons;

# not a strict model per se, but dehydrates and rehydrates into something that GameData will use
class GamePlayer():
	colorMappings = ["#FF8888","#8888FF","#FFCC55","#BBFFBB"];

	bgColorMappings = ["#FF8888","#8888FF","#FFCC55","#55CC55"];
	lightBgColorMappings = ["#FF8888","#8888FF","#FFCC55","#55CC55"];
	
	def initWithId(this, myId, myName) :
		this.playerId = myId;
		this.playerName = myName;
		this.aiModel = -1; # if 0 or higher, means the player is an AI using the given model

		this.hand = [];
		this.points = 0;

		this.playerDataVersion = 0; # used to prevent multiple submits
		this.passcode = "";

		this.playerCardsAddedToHand = [];
		this.playerCardsRemovedFromHand = [];

	def getCellBGColor(this):
		return "background-color:"+this.bgColorMappings[this.playerId];

	def getLightCellBGColor(this):
		return "background-color:"+this.lightBgColorMappings[this.playerId];

	def getGenericCellBGColor(this):
		matchBgColor = "#DDDDDD";
		if this.playerId % 2 == 1:
			matchBgColor = "#EEEEEE";
		return "background-color:"+matchBgColor;

	def __lt__(self, other):
		return self.points < other.points;

	def getName(this):
		return mark_safe('<span><b>' + this.playerName + "</b></span>"); # TODO: MAKE SURE PLAYER NAME ENTRY ISN'T TERRIBLE

	def printedHandString(this):
		handString = "";
		for card in this.hand:
			handString += str(card) + ", "; # yes this is just id for now

		if len(handString) > 0:
			return handString[:-2];
		return handString;

	def getDebugString(this):
		return "P" + str(this.playerId+1) + ": " + this.playerName + " - " + str(this.points) + "pts - [" + this.printedHandString() + "]";

	def __repr__(this):
		return this.getDebugString();

	def serializeToString(this):
		everything = [this.playerId, this.playerName, this.aiModel, this.hand, this.points, this.playerDataVersion, this.passcode, this.playerCardsAddedToHand, this.playerCardsRemovedFromHand];
		return str(everything);

	def deserializeFromString(this, everythingString):
		everything = literal_eval(everythingString);
		this.playerId = everything[0];
		this.playerName = everything[1];
		this.aiModel = everything[2];
		this.hand = everything[3];
		this.points = everything[4];
		this.playerDataVersion = everything[5];
		this.passcode = everything[6];
		this.playerCardsAddedToHand = everything[7];
		this.playerCardsRemovedFromHand = everything[8];

# not a strict model per se, but dehydrates and rehydrates into something that GameData will use
class GameMatch():
	def initNewMatch(this, myId, competitorList, randomizerList, playerCount) :
		this.matchId = myId;

		this.competitors = [];
		this.competitorsFinalCheer = [];
		this.competitorsBaseAbility = [];
		this.competitorsTotalAbility = [];
		this.competitorTotalBet = [];
		for competitor in competitorList:
			this.competitors.append(competitor);
			this.competitorsFinalCheer.append(0);
			this.competitorsBaseAbility.append(0);
			this.competitorsTotalAbility.append(0);
			this.competitorTotalBet.append(0);

		this.competitorRandomizers = randomizerList; # what randomizer card each competitor got for +ability

		this.playerSupported = []; # which competitor each player supported. -1 means they're still going
		this.playerCardsPlayed = []; # what cards each player played
		this.playerBetBonus = []; # what each player's bet bonus was (from withdrawing early)
		this.playerTotalBet = [];
		this.playerPendingActions = []; # what every player is going to do this turn
		this.playerPerformedActions = []; # what each player has done every turn in order
		this.playerPointsAfterMatch = []; 

		playerId = 0;
		while playerId < playerCount:
			this.playerSupported.append(-2); # -2 means still playing cards, -1 means done, 0+ means you didn't forget

			thisPlayerCardsPlayed = [];
			for competitor in competitorList:
				thisPlayerCardsPlayed.append([]);
			this.playerCardsPlayed.append(thisPlayerCardsPlayed);
			this.playerBetBonus.append(0);
			this.playerTotalBet.append(0);
			this.playerPerformedActions.append([]);
			this.playerPointsAfterMatch.append(0);

			playerId += 1;

		this.resetPlayerPendingActions();

		this.matchResolved = False; # mark this so we know to only resolve it once

	def playerIsDoneWithMatch(this, playerID): # true if player cannot play more cards
		return this.playerSupported[playerID] != -2; 

	def isReadyToDoBattle(this):
		return this.getCountOfPlayersStillInMatch() <= 0; # TODO - tell playe they got owned

	# pending action queue stuff
	def resetPlayerPendingActions(this):
		this.playerPendingActions = [];

	def doesPlayerHaveActionInQueue(this, playerID):
		for action in this.playerPendingActions:
			if action[0] == playerID:
				return True;
		return False;

	def readyToProcessCardPlays(this):
		return this.getCountOfPlayersStillInMatch() > 0 and this.getCountOfPlayersStillInMatch() == len(this.playerPendingActions);

	def getCountOfCardsPlayedByPlayer(this, playerID):
		count = 0;
		for playerCards in this.playerCardsPlayed[playerID]:
			count += len(playerCards);
		return count;
	# end pending action queue stuff

	def isPlayerLastOneNotSupporting(this, playerId): # TODO: rename
		count = this.getCountOfPlayersStillInMatch();

		if (count == 1 and this.playerIsDoneWithMatch(playerId) == False):
			return True;
		return False;

	def getCountOfPlayersStillInMatch(this):
		count = 0;

		i = 0;
		while i < len(this.playerSupported):
			if this.playerIsDoneWithMatch(i) == False:
				count += 1;
			i += 1;

		return count;

	def getCountOfPlayersSupportingCompetitor(this, compeId):
		count = 0;
		for playerSupport in this.playerSupported:
			if playerSupport == compeId:
				count += 1;
		return count;

	def getMatchWinner(this):
		highestAbility = -99;
		highestCheer = -99;
		highestRandomizer = -99;
		winner = -1;

		index = 0;
		while index < len(this.competitorsTotalAbility): #highest ability wins
			if (this.competitorsTotalAbility[index] > highestAbility):
				highestAbility = this.competitorsTotalAbility[index];
				winner = index;
			elif (this.competitorsTotalAbility[index] == highestAbility):
				winner = -1;

			index += 1;

		if (winner == -1): # break ties with cheer
			index = 0;
			while index < len(this.competitorsFinalCheer):
				if (this.competitorsTotalAbility[index] == highestAbility):
					if (this.competitorsFinalCheer[index] > highestCheer):
						highestCheer = this.competitorsFinalCheer[index];
						winner = index;
					elif (this.competitorsFinalCheer[index] == highestCheer):
						winner = -1;
				index += 1;

		if (winner == -1): # break ties with randomizer
			index = 0;
			while index < len(this.competitorsFinalCheer):
				if (this.competitorsTotalAbility[index] == highestAbility and this.competitorsFinalCheer[index] == highestCheer):
					if (this.competitorRandomizers[index] > highestRandomizer):
						highestRandomizer = this.competitorRandomizers[index];
						winner = index;
					elif (this.competitorRandomizers[index] == highestRandomizer):
						winner = -1;
				index += 1;

		return winner;

	def getDebugString(this):
		return "Match " + str(this.matchId) + ": Competitors " + str(this.competitors) + "";

	def __repr__(this):
		return this.getDebugString();

	def serializeToString(this):
		everything = [this.matchId, this.competitors, this.competitorRandomizers, this.playerSupported, this.playerCardsPlayed, this.playerBetBonus, this.matchResolved, this.competitorsFinalCheer, this.competitorsBaseAbility, this.competitorsTotalAbility, this.playerTotalBet, this.playerPendingActions, this.playerPerformedActions, this.competitorTotalBet, this.playerPointsAfterMatch];
		return str(everything);

	def deserializeFromString(this, everythingString):
		everything = literal_eval(everythingString);
		this.matchId = everything[0];
		this.competitors = everything[1];
		this.competitorRandomizers = everything[2];
		this.playerSupported = everything[3];
		this.playerCardsPlayed = everything[4];
		this.playerBetBonus = everything[5];
		this.matchResolved = everything[6];
		this.competitorsFinalCheer = everything[7];
		this.competitorsBaseAbility = everything[8];
		this.competitorsTotalAbility = everything[9];
		this.playerTotalBet = everything[10];
		this.playerPendingActions = everything[11];
		this.playerPerformedActions = everything[12];
		this.competitorTotalBet = everything[13];
		this.playerPointsAfterMatch = everything[14];