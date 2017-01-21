from django.http import HttpResponse, Http404
from copy import deepcopy
from ast import literal_eval;
from django.shortcuts import render

import random;
import json;
from tablesaltGame.models import *
from tablesaltGame.aiModels import *
from siteConstants import *

# TODO: how to kill infinite loops (i.e. when my code runs too long)

SUPPORTER_CARD_ID = 17; # nice constant

class UIMatch:
	# TODO: move
	def getRandomizerCardHTML(this, randomValue):
		cardId = str(randomValue);
		if randomValue == 0.5:
			cardId = "point5";
		elif randomValue == -1:
			cardId = "minus1";

		cardURL = settings.STATIC_URL + "/randomcards/" + str(cardId) + ".png";
		imgWidth = 80;

		return '<img src="'+cardURL+'" width="'+str(imgWidth)+'"/>';

	def __init__(this, gameManager, match):
		this.matchId = match.matchId;
		this.matchIdPlusOne = match.matchId + 1;
		this.isCurrentMatch = (this.matchId == gameManager.getCurrentMatch().matchId);

		# information for straight debugging purposes
		this.competitors = [];
		for competitor in match.competitors: # hydrate competitors for UI
			this.competitors.append(gameManager.getCardInDeckWithId(gameManager.allCompetitorCards, competitor));

		this.competitorRandomizers = match.competitorRandomizers;
		this.playerSupported = match.playerSupported;

		this.playerCardsPlayed = [];
		for playerCardsTriplet in match.playerCardsPlayed: # hydrate list of cards played
			thisPlayerCardsPlayed = [];
			for playerCards in playerCardsTriplet:
				cardsPlayed = [];
				for card in playerCards:
					cardsPlayed.append(gameManager.getCardInDeckWithId(gameManager.allBoostCards, card));
				thisPlayerCardsPlayed.append(cardsPlayed);
			this.playerCardsPlayed.append(thisPlayerCardsPlayed);

		this.playerBetBonus = match.playerBetBonus;
		this.matchResolved = match.matchResolved;
		this.competitorsFinalCheer = match.competitorsFinalCheer;
		this.competitorsBaseAbility = match.competitorsBaseAbility;
		this.competitorsTotalAbility = match.competitorsTotalAbility;
		this.playerTotalBet = match.playerTotalBet;
		this.playerPendingActions = match.playerPendingActions;
		this.playerPerformedActions = match.playerPerformedActions;
		this.competitorTotalBet = match.competitorTotalBet;
		this.playerPointsAfterMatch = match.playerPointsAfterMatch;

		# cool actually displayable UI things
		cardsPlayedOnCompetitor = [];
		this.competitorCheerAbilityValues = []; # TODO: lazy pairing with below
		this.competitorCheerAbilityStrings = []; #TODO: this is really competitor info
		this.competitorAbilityTables = [];

		this.uiSidebar = [];

		index = 0;
		while index < len(this.competitorsFinalCheer):
			cheer = this.competitorsFinalCheer[index];
			baseAbility = this.competitorsBaseAbility[index];
			name = this.competitors[index].name;
			randomAbility = abs(this.competitorsTotalAbility[index]) - abs(this.competitorsBaseAbility[index]); # to fix under reversal
			totalAbility = this.competitorsTotalAbility[index];
			if (totalAbility < 0): # can only happen under reversal
				cheer *= -1;

			finalCheerStr = str(cheer) + " cheer";
			if randomAbility > 0:
				finalPowerStr = str(baseAbility) + " (+" + str(randomAbility) + ") = " + str(totalAbility) + " ability"; 
			else:
				finalPowerStr = str(baseAbility) + " (-" + str(abs(randomAbility)) + ") = " + str(totalAbility) + " ability"; 

			cheerAbilityStrings = [];

			# write who supported
			wonMatch = (index == match.getMatchWinner());

			playerIndex = 0;
			playersSupporting = [];
			while playerIndex < len(this.playerSupported):
				if this.playerSupported[playerIndex] == index:
					playersSupporting.append(playerIndex);
				playerIndex += 1;

			supportString = "";

			if this.matchResolved:
				supportString += "<big><big><big>&#128100;" + str(totalAbility) + "</big></big></big> &#128227;" + str(cheer) + "" +" &#9733;" + str(this.competitorTotalBet[index])

			supportColor = "background-color:#CCCCCC";
			if len(playersSupporting) > 0:
				supportColor = "background-color:#FFFFFF";
				if len(playersSupporting) == 1:
					 supportColor = gameManager.players[playersSupporting[0]].getLightCellBGColor()

			# draw cheer as a power meter
			# TODO: clean up header string, which shows all competitor info now

			abilityTableString = "<table style='display:inline-table;vertical-align:top;'>";
			cheerTuples = literal_eval(this.competitors[index].cheerTrackValues);
			for cheerTuple in cheerTuples:
				cheerValue = int(cheerTuple[1]);
				abilityValue = int(cheerTuple[0]);

				cheerColor = "background-color:#BBBBBB";
				if (baseAbility == abilityValue and this.matchResolved):
					cheerColor = "background-color:#FFFF77";

				abilityTableString += "<tr style='text-align: center; min-width:64px;" + cheerColor + "'><td>&#128227;"+str(cheerValue)+" &#128100;" + str(abilityValue) + "</td></tr>"
			abilityTableString += "</table>";

			tableString = "";
			if (this.matchResolved):
				tableString = "<table><tr><td style='text-align: center'><b>"+supportString+"</b></td>";

				'''	TODO: we don't show random here rn
				if this.matchResolved:
					tableString += "<td style='text-align: center'>"
					if randomAbility >= 0:
						tableString += " + " + str(randomAbility);
					else:
						tableString += " - " + str(abs(randomAbility));
					tableString += "</td>"'''

				tableString += "</tr></table>";

			cheerAbilityStrings.append([tableString, supportColor, ""])

			# sort characters by ability
			insertIndex = 0;
			for value in this.competitorCheerAbilityValues:
				if value > totalAbility:
					insertIndex += 1;

			insertIndex = 99; # TODO: DO NOT SORT FOR NOW IT'S BROKEN
			if insertIndex >= len(this.competitorCheerAbilityValues):
				this.competitorCheerAbilityStrings.append(cheerAbilityStrings);
				this.competitorCheerAbilityValues.append(totalAbility);
				if this.matchResolved:
					cardsPlayedOnCompetitor.append([[this.competitors[index].getRulesCardHTML() + abilityTableString,"", "optionTarget" + str(index)],[this.getRandomizerCardHTML(randomAbility),"", ""]]);
				else:
					cardsPlayedOnCompetitor.append([[this.competitors[index].getRulesCardHTML() + abilityTableString,"", "optionTarget" + str(index)]]);
			'''else:
				this.competitorCheerAbilityStrings.insert(insertIndex, cheerAbilityStrings);
				this.competitorCheerAbilityValues.insert(insertIndex, totalAbility);
				if this.matchResolved:
					cardsPlayedOnCompetitor.insert(insertIndex, [[this.competitors[index].getRulesCardHTML(),"", "optionTarget" + str(index)],[this.getRandomizerCardHTML(randomAbility),"", ""]]);
				else:
					cardsPlayedOnCompetitor.insert(insertIndex, [[this.competitors[index].getRulesCardHTML(),"", "optionTarget" + str(index)]]);
'''
			index += 1;

		somePlayerHadAction = True;
		actionIndex = 0;
		while somePlayerHadAction:
			somePlayerHadAction = False;

			playerIndex = 0;
			while playerIndex < len(this.playerPerformedActions):
				if actionIndex < len(this.playerPerformedActions[playerIndex]):
					somePlayerHadAction = True;
					showCardName = this.matchResolved or playerIndex == gameManager.selectedPlayerId;

					action = this.playerPerformedActions[playerIndex][actionIndex];
					playedCard = gameManager.getCardInDeckWithId(gameManager.allBoostCards, action[0]);
					if playedCard.abilityType == AbilityEnum.ABILITY_PLAY_FACE_UP or playedCard.abilityType == AbilityEnum.ABILITY_SUPPORTER:
						showCardName = True;

					if showCardName:
						cardsPlayedOnCompetitor[action[1]].append([playedCard.getPlayedCardHTML(playerIndex), gameManager.players[playerIndex].getLightCellBGColor(), ""]);
					else:
						cardsPlayedOnCompetitor[action[1]].append([playedCard.getBackCardHTML(playerIndex), gameManager.players[playerIndex].getLightCellBGColor(), ""]);

				playerIndex += 1;

			actionIndex += 1;

		# TODO: this is a hack to put all the cards played in one table cell for now
		newCardsPlayedList = [];
		for competitor in cardsPlayedOnCompetitor:
			cardHTMLs = "";
			for card in competitor:
				cardHTMLs += card[0] + " "; 
			competitor = [[cardHTMLs, "background-color:#DDDDDD", competitor[0][2]]];
			newCardsPlayedList.append(competitor);
		cardsPlayedOnCompetitor = newCardsPlayedList;

		# interlace the above 2
		index = 0;
		newCompeCheerAbilityStrings = [];
		while index < len(this.competitorCheerAbilityStrings):
			# TODO: clean up lazy interlacing of two pairs per row
			if index + 1 < len(this.competitorCheerAbilityStrings):
				mergedTwo = [this.competitorCheerAbilityStrings[index][0], this.competitorCheerAbilityStrings[index+1][0]]
				if (this.matchResolved): # lazy hack - don't show header if not resolved
					newCompeCheerAbilityStrings.append(mergedTwo);
				cardsPlayedOnCompetitor[index][0][1] = this.competitorCheerAbilityStrings[index][0][1];
				cardsPlayedOnCompetitor[index+1][0][1] = this.competitorCheerAbilityStrings[index+1][0][1];
				mergedTwo = [cardsPlayedOnCompetitor[index][0], cardsPlayedOnCompetitor[index+1][0]]
				newCompeCheerAbilityStrings.append(mergedTwo);
				index += 2;
			else:
				cardsPlayedOnCompetitor[index][0][1] = this.competitorCheerAbilityStrings[index][0][1];
				if (this.matchResolved): # lazy hack - don't show header if not resolved
					newCompeCheerAbilityStrings.append(this.competitorCheerAbilityStrings[index]);
				newCompeCheerAbilityStrings.append(cardsPlayedOnCompetitor[index]);
				index += 1;
		this.competitorCheerAbilityStrings = newCompeCheerAbilityStrings;

		# show what players did
		this.performedActionStrings = [];
		index = 0;
		actionBgColors = ["background-color:#EEEEEE", "background-color:#DDDDDD"];

		unsortedPlayerScoreHTML = [];
		while index < len(this.playerPerformedActions):
			playerActionStrings = [];
			playerSupportedIndex = -1;
			showCardName = this.matchResolved or index == gameManager.selectedPlayerId;

			if (gameManager.players[index].aiModel >= 0):
				playerNumberName = "[AI" + str(index + 1) + "]";
			else:
				playerNumberName = "[P" + str(index + 1) + "]";

			playerActionStrings.append([playerNumberName + " " + gameManager.players[index].playerName, gameManager.players[index].getCellBGColor()]);

			playerPoints = this.playerPointsAfterMatch[index];
			pointsGained = 0;
			if this.matchResolved == False:
				playerPoints = gameManager.players[index].points;
			else:
				if (this.matchId == 0): # first match
					pointsGained = this.playerPointsAfterMatch[index];
				else:
					prevMatch = gameManager.matches[this.matchId-1];
					pointsGained = this.playerPointsAfterMatch[index] - prevMatch.playerPointsAfterMatch[index];

			if pointsGained == 0:
				playerActionStrings.append(["&#9734;" + str(playerPoints) + "", "background-color:#CCCCCC"]);
			else:
				playerActionStrings.append(["&#9734;" + str(playerPoints) + " (+&#9734;" + str(pointsGained) + ")", "background-color:#CCCCCC"]);

			for action in this.playerPerformedActions[index]:
				if (action[0] != -1):
					if (action[0] == SUPPORTER_CARD_ID):
						playerSupportedIndex = action[1];

			unsortedPlayerScoreHTML.append([playerActionStrings, playerPoints])
			index += 1;

		if this.matchResolved:
			this.uiSidebar.append([["<b>Match Results</b>", ""]])

			competitorValueTuples = [];
			index = 0;
			while index < len(this.competitorsFinalCheer):
				cheer = this.competitorsFinalCheer[index];
				bet = this.competitorTotalBet[index];
				baseAbility = this.competitorsBaseAbility[index];
				name = this.competitors[index].name;
				randomAbility = abs(this.competitorsTotalAbility[index]) - abs(this.competitorsBaseAbility[index]); # to fix under reversal
				totalAbility = this.competitorsTotalAbility[index];

				playersSupporting = [];
				playerIndex = 0;
				while playerIndex < len(this.playerSupported):
					if this.playerSupported[playerIndex] == index:
						playersSupporting.append(playerIndex);
					playerIndex += 1;

				supportColor = "background-color:#CCCCCC";
				if len(playersSupporting) > 0:
					supportColor = "background-color:#FFFFFF";
					if len(playersSupporting) == 1:
						 supportColor = gameManager.players[playersSupporting[0]].getLightCellBGColor()

				competitorValueTuples.append([totalAbility, cheer, bet, supportColor, randomAbility])

				index += 1;

			isWinner = True;
			while len(competitorValueTuples) > 0:
				toRemove = None;
				highestScore = -999;
				for compeTuple in competitorValueTuples:
					thisScore = compeTuple[0] * 100 + compeTuple[1] * 10 + compeTuple[4];
					if thisScore > highestScore:
						toRemove = compeTuple;
						highestScore = thisScore;

				sideString = "";
				if isWinner:
					isWinner = False;
					sideString = "&#128100;"+str(toRemove[0]) + " &#128227;" + str(toRemove[1]) + " &#9734;" + str(toRemove[2]);
				else:
					sideString = "&#128100;"+str(toRemove[0]) + " &#128227;" + str(toRemove[1]);

				this.uiSidebar.append([[sideString, toRemove[3], ""]]);
				competitorValueTuples.remove(toRemove);

		this.uiSidebar.append([["<b>Scores</b>", ""]])
		while len(unsortedPlayerScoreHTML) > 0:
			toRemove = None;
			highestScore = -999;
			for playerHTML in unsortedPlayerScoreHTML:
				if playerHTML[1] > highestScore:
					toRemove = playerHTML;
					highestScore = playerHTML[1];

			this.uiSidebar.append(toRemove[0]);
			unsortedPlayerScoreHTML.remove(toRemove);



class UIPlayer:
	def __init__(this, gameManager, player):
		this.playerId = player.playerId;
		this.playerName = player.playerName;
		this.aiModel = player.aiModel;

		this.hand = [];
		for card in player.hand: # hydrate player's hand for UI
			this.hand.append(gameManager.getCardInDeckWithId(gameManager.allBoostCards, card));
		this.handVisible = this.playerId == gameManager.selectedPlayerId;
		this.cardsInHand = len(this.hand);

		this.points = player.points;

		this.cellBGColor = player.getCellBGColor();

class GameManager:
	def setup(this, selectedPlayerId, myGameData, notificationText):
		this.gameSaveNeeded = False;

		this.notificationText = notificationText;
		this.gameData = myGameData;
		this.selectedPlayerId = int(selectedPlayerId) - 1; # correct bc 0s
		this.selectedPlayerIdPlusOne = this.selectedPlayerId + 1;
		this.curPlayerName = "";
		
		this.allBoostCards = BoostCard.objects.all();
		this.allCompetitorCards = CompetitorCard.objects.all();

		this.hydratedBoostCardDeck = this.getRehydratedBoostCardDeck(literal_eval(this.gameData.boostCardDeck));
		this.hydratedCompetitorCardDeck = this.getRehydratedCompetitorCardDeck(literal_eval(this.gameData.competitorCardDeck));
		this.gameConfiguration = None;

		this.players = this.gameData.deserializePlayers();
		this.activePlayer = this.players[this.selectedPlayerId];

		this.matches = this.gameData.deserializeMatches();

		# setup things
		matchingGameConfigs = GameConfiguration.objects.filter(id=this.gameData.configurationId);
		if (len(matchingGameConfigs) != 1):
			raise Http404(str(len(matchingGameConfigs)) + " game configs with id " + str(this.gameData.configurationId) + " found, expected 1");
		this.gameConfiguration = matchingGameConfigs[0];

		this.hydratedRandomizers = literal_eval(this.gameConfiguration.randomizerValues);
		this.hydratedBetTrack = literal_eval(this.gameConfiguration.betTrackValues);

		if (this.selectedPlayerId < 0 or this.selectedPlayerId >= len(this.players)):
			raise Http404("Selected player ID " + str(this.selectedPlayerId) + " out of bounds!");
		
	def reloadUIVariables(this):
		currentMatch = this.getCurrentMatch();
		this.UIcurrentMatchId = currentMatch.matchId;

		this.UImatches = [];
		for match in this.matches:
			uiMatch = UIMatch(this, match);
			this.UImatches.append(uiMatch);
		this.UImatches.reverse(); # make them go backwards for better UI surfacing

		this.UImatchesInGame = this.gameConfiguration.numberOfMatches;

		this.UIplayers = [];
		for player in this.players:
			uiPlayer = UIPlayer(this, player);

			this.UIplayers.append(uiPlayer);

		this.UIboostDeckCardCount = len(this.hydratedBoostCardDeck);
		this.UIplayerCellColor = this.UIplayers[this.selectedPlayerId].cellBGColor[17:];

		this.UIcardPlayDescriptions = [];
		# active player must play cards
		this.UIactivePlayerCanPlayCard = this.doesPlayerNeedToPlayCard(this.selectedPlayerId);
		if this.UIactivePlayerCanPlayCard: # get what cards can be played
			this.UIcardPlayOptions = [];
			this.UIcardTargetOptions = [];

			# get the cards you can play 
			cardIndex = 0;
			while cardIndex < len(this.activePlayer.hand):
				boostCard = this.getCardInDeckWithId(this.allBoostCards, this.activePlayer.hand[cardIndex]);

				cardBgColor = ";background-color:#CCCCCC";
				#this.UIcardPlayOptions.append([cardIndex, boostCard.name, boostCard.textDescription, cardBgColor]);
				this.UIcardPlayOptions.append([cardIndex, boostCard.getRulesCardHTML(this.selectedPlayerId), "", cardBgColor])
				this.UIcardPlayDescriptions.append(boostCard.getHelperDescription()); 
				cardIndex += 1;

			# get the competitors you can support
			competitorIndex = 0;
			while competitorIndex < len(currentMatch.competitors):
				compeCard = this.getCardInDeckWithId(this.allCompetitorCards, currentMatch.competitors[competitorIndex]);

				# can't support someone who already is
				canSupportCompe = True;
				for supportingId in currentMatch.playerSupported:
					if supportingId == competitorIndex:
						canSupportCompe = False;

				if canSupportCompe:
					this.UIcardTargetOptions.append([competitorIndex, compeCard.name])
				competitorIndex += 1;

			# note: stop playing cards is now just hard-baked into rendergame template

		this.UIdraftingCards = this.playersAreCurrentlyDraftingCards();
		this.UIactivePlayerMustDraftCard = this.UIdraftingCards and len(this.players[this.selectedPlayerId].playerCardsAddedToHand) <= currentMatch.matchId;

		this.UIcardRemoveDescriptions = {};
		this.UIcardAddDescriptions = {};
		if this.UIactivePlayerMustDraftCard: # get draft card options			
			this.UIcardRemoveOptions = [];
			this.UIcardAddOptions = [];

			# get the cards you can remove
			cardIndex = 0;
			while cardIndex < len(this.activePlayer.hand):
				boostCard = this.getCardInDeckWithId(this.allBoostCards, this.activePlayer.hand[cardIndex]);

				cardBgColor = ";background-color:#CCCCCC";
				if (boostCard.id == SUPPORTER_CARD_ID):
					cardBgColor = ";background-color:#CCCCFF";
				#this.UIcardRemoveOptions.append([boostCard.id, boostCard.name, boostCard.textDescription, cardBgColor]);
				this.UIcardRemoveOptions.append([boostCard.id, boostCard.getRulesCardHTML(this.selectedPlayerId), "", cardBgColor])
				this.UIcardRemoveDescriptions[boostCard.id] = boostCard.getHelperDescription(); 

				cardIndex += 1;
			this.UIcardRemoveOptions.append([100, "No change", "Keep your hand the same.", ";background-color:#CCCCCC"]);

			# get the cards you can add
			for card in this.hydratedBoostCardDeck:
				if card.id not in this.activePlayer.hand: # lazy logic but whatever
					cardBgColor = ";background-color:#CCCCCC";
					#this.UIcardAddOptions.append([card.id, card.name, card.textDescription, cardBgColor]);
					this.UIcardAddOptions.append([card.id, card.getRulesCardHTML(this.selectedPlayerId), "", cardBgColor])
					this.UIcardAddDescriptions[card.id] = card.getHelperDescription(); 

		this.UIcardPlayDescriptions = json.dumps(this.UIcardPlayDescriptions);
		this.UIcardAddDescriptions = json.dumps(this.UIcardAddDescriptions);
		this.UIcardRemoveDescriptions = json.dumps(this.UIcardRemoveDescriptions);

	def getRehydratedBoostCardDeck(this, cardArray):
		deck = [];
		
		for cardId in cardArray:
			for card in this.allBoostCards:
				if card.id == cardId:
					deck.append(card);
		return deck;

	def getRehydratedCompetitorCardDeck(this, cardArray):
		deck = [];
		for cardId in cardArray:
			for card in this.allCompetitorCards:
				if card.id == cardId:
					deck.append(card);
		return deck;

	def getCardInDeckWithId(this, deck, cardId):
		for card in deck:
			if card.id == cardId:
				return card;
		return None;

	def getPositionName(this, pos) :
		if pos == 0:
			return "1st";
		elif pos == 1:
			return "2nd";
		elif pos == 2:
			return "3rd";
		else:
			return str(pos+1) + "th";

	def doFirstTimeGameSetupIfNeeded(this):
		if len(this.matches) == 0: 
			this.prepareNextMatch();

	def dehydrateCardDeck(this, deck):
		dehydrated = [];
		for card in deck:
			dehydrated.append(card.id);
		return dehydrated;

	def saveGame(this):
		this.gameData.serializeAndSetPlayers(this.players);
		this.gameData.serializeAndSetMatches(this.matches);

		this.gameData.boostCardDeck = this.dehydrateCardDeck(this.hydratedBoostCardDeck);
		this.gameData.competitorCardDeck = this.dehydrateCardDeck(this.hydratedCompetitorCardDeck);

		# data version is now calculated progmatically
		currentMatch = this.getCurrentMatch();
		maxCards = 0;
		for actionPlayer in currentMatch.playerPerformedActions:
			if len(actionPlayer) > maxCards:
				maxCards = len(actionPlayer);
		this.gameData.dataVersion = currentMatch.matchId + maxCards;

		this.gameData.save();

	def createPlayerHands(this, addSupporter):
		# deal initial hands to everyone
		for player in this.players:
			player.hand = [];

			# get their full boost deck, except for advanced cards
			playerDeck = [];
			for card in this.hydratedBoostCardDeck:
				if card.advancedCard == False:
					playerDeck.append(card.id);

			# players get their whole deck every turn
			for card in playerDeck:
				# TODO: don't get advanced cards they haven't drafted
				player.hand.append(card);

			# cards you drafted
			for cardId in player.playerCardsAddedToHand: 
				player.hand.append(cardId);
			for cardId in player.playerCardsRemovedFromHand: 
				player.hand.remove(cardId);

			# give everyone their supporter card in hand 
			if SUPPORTER_CARD_ID not in player.hand and addSupporter:
				player.hand.append(SUPPORTER_CARD_ID);

			# TODO: sort hands

	def prepareNextMatch(this):
		this.createPlayerHands(True);

		# create starter match
		newMatch = this.createNewMatch();
		this.matches.append(newMatch);

		# save
		this.gameSaveNeeded = True;

	def createNewMatch(this): # returns a new GameMatch
		matchId = len(this.matches);

		matchCompetitors = [];
		count = 0;
		while count < len(this.players): # same amount of competitors as players now
			cardDealt = this.hydratedCompetitorCardDeck[0];
			this.hydratedCompetitorCardDeck = this.hydratedCompetitorCardDeck[1:];

			matchCompetitors.append(cardDealt.id);
			count += 1;

		matchRandomizers = [];
		for randomizer in this.hydratedRandomizers:
			matchRandomizers.append(randomizer);
		random.shuffle(matchRandomizers);

		newMatch = GameMatch();
		newMatch.initNewMatch(matchId, matchCompetitors, matchRandomizers, len(this.players));
		return newMatch;

	def getCurrentMatch(this):
		currentMatch = this.matches[-1];
		return currentMatch;

	def isGameOver(this):
		return len(this.matches) >= this.gameConfiguration.numberOfMatches and this.getCurrentMatch().matchResolved;

	def doesPlayerHaveToDraftCard(this, playerId):
		currentMatch = this.getCurrentMatch();
		return this.playersAreCurrentlyDraftingCards() and len(this.players[playerId].playerCardsAddedToHand) <= currentMatch.matchId;

	def doesPlayerNeedToPlayCard(this, playerId):
		currentMatch = this.getCurrentMatch();

		if (this.isGameOver()):
			return False;

		if (currentMatch.matchResolved): # match is over, you do not
			return False;

		if (currentMatch.playerIsDoneWithMatch(playerId)): # you've already finished
			return False;

		if (currentMatch.doesPlayerHaveActionInQueue(playerId)):
			return False; # you already played an action

		return True;

	def playersHaveDraftedCardPostMatch(this, match):
		cardsDrafted = match.matchId;
		for player in this.players:
			if len(player.playerCardsAddedToHand) <= cardsDrafted:
				return False;

		return True;

	def playersAreCurrentlyDraftingCards(this):
		if (this.isGameOver()):
			return False;

		currentMatch = this.getCurrentMatch();
		return currentMatch.matchResolved and this.playersHaveDraftedCardPostMatch(currentMatch) == False;

	def advanceGameStateIfPossible(this):
		stateChanged = False;
		currentMatch = this.getCurrentMatch();

		if (currentMatch.matchResolved == False): # match isn't done, wait until we can make it done
			if (currentMatch.readyToProcessCardPlays()):
				numberOfPlayersDropped = len(this.players) - currentMatch.getCountOfPlayersStillInMatch();
				currentBetTier = this.hydratedBetTrack[numberOfPlayersDropped];

				# process actions
				for action in currentMatch.playerPendingActions:
					playerID = action[0];
					cardIndex = action[1];
					competitorId = action[2];

					cardPlayed = this.players[playerID].hand[cardIndex];
					currentMatch.playerCardsPlayed[playerID][competitorId].append(cardPlayed); # play the card
					this.players[playerID].hand.pop(cardIndex)	# remove index from your hand

					if cardPlayed == SUPPORTER_CARD_ID:
						currentMatch.playerSupported[playerID] = competitorId;
						currentMatch.playerBetBonus[playerID] = 0; # bet bonus doesn't exist anymore
						this.players[playerID].hand = []; # [cardPlayed];

					currentMatch.playerPerformedActions[playerID].append([cardPlayed, competitorId]);

				currentMatch.resetPlayerPendingActions();
				this.gameSaveNeeded = True;
				stateChanged = True;

			if (currentMatch.isReadyToDoBattle()):
				this.resolveCurrentMatch();

				this.createPlayerHands(False); # recreate player hands for drafting

				this.gameSaveNeeded = True;
				stateChanged = True;

		if (this.isGameOver()): # end here if the game's over
			return stateChanged;

		if (currentMatch.matchResolved == True): # match is done, goto next
			if (this.playersHaveDraftedCardPostMatch(currentMatch)):
				this.prepareNextMatch(); 
				stateChanged = True;

		return stateChanged;

	def resolveCurrentMatch(this):
		currentMatch = this.getCurrentMatch();

		reversalActive = False;
		underdogCount = [];
		for competitor in currentMatch.competitors:
			underdogCount.append(0);

		inverterActive = [];
		for competitor in currentMatch.competitors:
			inverterActive.append(False);

		cheerCollabCount = [];
		totalCheerCollabs = 0;
		for competitor in currentMatch.competitors:
			cheerCollabCount.append(0);
		cheerCollabCountByPlayer = []
		for player in this.players:
			mimicArray = [];
			for competitor in currentMatch.competitors:
				mimicArray.append(0);
			cheerCollabCountByPlayer.append(mimicArray);

		mimicCount = []
		for player in this.players:
			mimicArray = [];
			for competitor in currentMatch.competitors:
				mimicArray.append(0);
			mimicCount.append(mimicArray);
		cheerGainCount = [];
		for player in this.players:
			mimicArray = [];
			for competitor in currentMatch.competitors:
				mimicArray.append(0);
			cheerGainCount.append(mimicArray);
		backupBet = [];
		for player in this.players:
			mimicArray = [];
			for competitor in currentMatch.competitors:
				mimicArray.append(0);
			backupBet.append(mimicArray);

		# sweep for inverters first
		index = 0;
		while index < len(currentMatch.playerCardsPlayed):
			thisPlayerCards = currentMatch.playerCardsPlayed[index];

			competitorIndex = 0;
			while competitorIndex < len(thisPlayerCards):
				thisCards = thisPlayerCards[competitorIndex];
				for cardId in thisCards:
					card = this.getCardInDeckWithId(this.allBoostCards, cardId);

					if card.abilityType == AbilityEnum.ABILITY_INVERTER:
						inverterActive[competitorIndex] = (inverterActive[competitorIndex] == False); # toggle inverter
				competitorIndex += 1;
			index += 1;

		# apply cards now
		index = 0;
		while index < len(currentMatch.playerCardsPlayed):
			thisPlayerCards = currentMatch.playerCardsPlayed[index];

			competitorIndex = 0;
			while competitorIndex < len(thisPlayerCards):
				thisCards = thisPlayerCards[competitorIndex];
				for cardId in thisCards:
					card = this.getCardInDeckWithId(this.allBoostCards, cardId);

					cheer = card.cheerAmount;
					bet = card.betAmount;

					if inverterActive[competitorIndex]:
						cheer = card.betAmount;
						bet = card.cheerAmount;

					if card.abilityType == AbilityEnum.ABILITY_SUPPORTER: # this is who you're repping!
						currentMatch.playerSupported[index] = competitorIndex; 
						bet = 5; # TODO: hardcoded to avoid inverter lol

					elif card.abilityType == AbilityEnum.ABILITY_CHEER_COLLAB:
						totalCheerCollabs += 1;
						cheerCollabCount[competitorIndex] += 1;
						cheerCollabCountByPlayer[index][competitorIndex] += 1;

					elif card.abilityType == AbilityEnum.ABILITY_CHEER_SOLO: # X+1 if you're the only one
						if currentMatch.playerSupported[index] > -1:
							valid = (currentMatch.getCountOfPlayersSupportingCompetitor(competitorIndex) == 1 and competitorIndex == currentMatch.playerSupported[index]);
							if valid:
								cheer = len(this.players) + 1;

					elif card.abilityType == AbilityEnum.ABILITY_BET_SOLO:
						if currentMatch.playerSupported[index] > -1:
							valid = (currentMatch.getCountOfPlayersSupportingCompetitor(competitorIndex) == 1 and competitorIndex == currentMatch.playerSupported[index]);
							if valid:
								bet = len(this.players);

					elif card.abilityType == AbilityEnum.ABILITY_BET_BOOST: # all players bet up regardless of where or what
						betIndex = 0;
						while betIndex < len(currentMatch.playerTotalBet):
							currentMatch.playerTotalBet[betIndex] += bet;
							betIndex += 1;
						bet = 0;

					elif card.abilityType == AbilityEnum.ABILITY_BET_BALANCE: # bet +, bet - ability at end
						TODO_thisCardIsDeprecated = True;

					elif card.abilityType == AbilityEnum.ABILITY_REVERSAL:
						reversalActive = (reversalActive == False); # toggle reversal

					elif card.abilityType == AbilityEnum.ABILITY_UNDERDOG: # +1 ability if not tie/have highest ability
						underdogCount[competitorIndex] += 1;

					elif card.abilityType == AbilityEnum.ABILITY_MIMIC:
						mimicCount[index][competitorIndex] += 1;

					elif card.abilityType == AbilityEnum.ABILITY_FREE_POINTS:
						this.players[index].points += 2; # TODO: don't hardcode

					elif card.abilityType == AbilityEnum.ABILITY_BACKUP_PLAN:
						backupBet[index][competitorIndex] += 4; # TODO: don't hardcode

					elif card.abilityType == AbilityEnum.ABILITY_NULLIFY_IF_NOT_ONLY_CARD:
						cardWorks = True;

						# sweep for other cards by player
						index2 = 0;
						while index2 < len(currentMatch.playerCardsPlayed):
							if index2 == index: # check out your cards only
								thisPlayerCards22 = currentMatch.playerCardsPlayed[index2];

								thisCards22 = thisPlayerCards22[competitorIndex];
								for cardId22 in thisCards22:
									card2 = this.getCardInDeckWithId(this.allBoostCards, cardId22);

									if card2.id != card.id and card2.id != SUPPORTER_CARD_ID:
										cardWorks = False;

							index2 += 1;

						if cardWorks == False:
							bet = 0;
							cheer = 0;

					elif card.abilityType == AbilityEnum.ABILITY_SOLO_STAR:
						soloStarWorks = True;

						# sweep for other +cheer cards
						index2 = 0;
						while index2 < len(currentMatch.playerCardsPlayed):
							if index2 != index: # check other player cards
								thisPlayerCards22 = currentMatch.playerCardsPlayed[index2];

								thisCards22 = thisPlayerCards22[competitorIndex];
								for cardId22 in thisCards22:
									card2 = this.getCardInDeckWithId(this.allBoostCards, cardId22);

									cheer2 = card2.cheerAmount;
									if inverterActive[competitorIndex]:
										cheer2 = card2.betAmount;
									if (cheer2 > 0):
										soloStarWorks = False;

							index2 += 1;

						if soloStarWorks == False:
							bet = 0;
							cheer = 0;

					currentMatch.competitorsFinalCheer[competitorIndex] += cheer; # always cheer
					cheerGainCount[index][competitorIndex] += cheer;

					currentMatch.competitorTotalBet[competitorIndex] += bet;

				competitorIndex += 1;

			index += 1;

		# cheer collab bonus
		competitorIndex = 0;
		while competitorIndex < len(currentMatch.competitorsBaseAbility):
			currentMatch.competitorsFinalCheer[competitorIndex] += cheerCollabCount[competitorIndex] * totalCheerCollabs;
			competitorIndex += 1;
		# this is just notation for mimic
		playerIndex = 0;
		while playerIndex < len(cheerCollabCountByPlayer):
			competitorIndex = 0;
			cheerCollabPlayers = cheerCollabCountByPlayer[playerIndex];

			while competitorIndex < len(cheerCollabPlayers):
				cheerGainCount[playerIndex][competitorIndex] += cheerCollabPlayers[competitorIndex] * totalCheerCollabs;
				competitorIndex += 1;
			playerIndex += 1;

		# do mimics now
		playerIndex = 0;
		while playerIndex < len(mimicCount): # this probably breaks under multiple mimics. please don't
			competitorIndex = 0;
			playerIndexes = mimicCount[playerIndex];

			while competitorIndex < len(currentMatch.competitorsBaseAbility):

				if playerIndexes[competitorIndex] > 0: #mimic is happening alert
					newCompeIndex = 0;
					gainCheer = cheerGainCount[playerIndex][competitorIndex];

					while newCompeIndex < len(currentMatch.competitorsBaseAbility): 
						if newCompeIndex == competitorIndex:
							currentMatch.competitorsFinalCheer[newCompeIndex] -= gainCheer;
						else:
							currentMatch.competitorsFinalCheer[newCompeIndex] += gainCheer;
						newCompeIndex += 1;
				competitorIndex += 1;

			playerIndex += 1;

		# calculate base ability now
		competitorIndex = 0;
		while competitorIndex < len(currentMatch.competitorsBaseAbility):
			card = this.getCardInDeckWithId(this.allCompetitorCards, currentMatch.competitors[competitorIndex]);

			currentMatch.competitorsBaseAbility[competitorIndex] = card.getAbilityWithCheerValue(currentMatch.competitorsFinalCheer[competitorIndex]);
			competitorIndex += 1;

		# add underdog bonus now
		competitorIndex = 0;
		maxBaseAbility = 0;
		for ability in currentMatch.competitorsBaseAbility:
			if ability > maxBaseAbility:
				maxBaseAbility = ability;
		while competitorIndex < len(currentMatch.competitorsBaseAbility):
			if underdogCount[competitorIndex] > 0 and currentMatch.competitorsBaseAbility[competitorIndex] < maxBaseAbility:
				currentMatch.competitorsBaseAbility[competitorIndex] += underdogCount[competitorIndex]
			competitorIndex += 1;

		# calculate total ability now
		competitorIndex = 0;
		while competitorIndex < len(currentMatch.competitorsBaseAbility):
			baseAbility = currentMatch.competitorsBaseAbility[competitorIndex];

			currentMatch.competitorsTotalAbility[competitorIndex] = baseAbility + currentMatch.competitorRandomizers[competitorIndex];
			competitorIndex += 1;

		# do reversal if appropriate by multiplying by -1
		if (reversalActive): 
			competitorIndex = 0;
			while competitorIndex < len(currentMatch.competitorsBaseAbility):
				currentMatch.competitorsTotalAbility[competitorIndex] *= -1;
				currentMatch.competitorsFinalCheer[competitorIndex] *= -1;
				competitorIndex += 1;

		# assign competitor bet to each player
		# TODO: divide when people split
		index = 0;
		while index < len(this.players):
			if (currentMatch.playerSupported[index] > -1):
				playersSupporting = currentMatch.getCountOfPlayersSupportingCompetitor(currentMatch.playerSupported[index]);
				competitorBet = currentMatch.competitorTotalBet[currentMatch.playerSupported[index]];

				currentMatch.playerTotalBet[index] = competitorBet / playersSupporting;
			index += 1;

		# pay out players
		matchWinner = currentMatch.getMatchWinner();
		index = 0;
		while index < len(this.players):
			if (currentMatch.playerSupported[index] > -1 and currentMatch.playerSupported[index] == matchWinner):
				player = this.players[index];
				player.points += currentMatch.playerTotalBet[index]; # earn points equal to bet. yea
			elif (currentMatch.playerSupported[index] > -1 and currentMatch.playerSupported[index] != matchWinner):
				player = this.players[index];
				player.points += backupBet[index][matchWinner];

			player = this.players[index];
			currentMatch.playerPointsAfterMatch[index] = player.points;
			index += 1;

		# remove supporter cards from people who didn't play it
		for player in this.players:
			while SUPPORTER_CARD_ID in player.hand:
				player.hand.remove(SUPPORTER_CARD_ID);

		# finalize match
		currentMatch.matchResolved = True;

# returns [shouldPersistSelectedInfo, text, game manager]
def processPostedAction(request, gameManager, playerID):
	actionTuple = {};

	if "optionCard" in request.POST:
		actionTuple["optionCard"] = int(request.POST["optionCard"]);
	if "optionAddCard" in request.POST:
		actionTuple["optionAddCard"] = int(request.POST["optionAddCard"]);
	if "optionRemoveCard" in request.POST:
		actionTuple["optionRemoveCard"] = int(request.POST["optionRemoveCard"]);
	if "optionTarget" in request.POST:
		actionTuple["optionTarget"] = int(request.POST["optionTarget"]);
	if "playerDataVersion" in request.POST:
		actionTuple["playerDataVersion"] = int(request.POST["playerDataVersion"]);

	return processPlayerAction(actionTuple, gameManager, playerID);

def processPlayerAction(actionTuple, gameManager, playerID):
	saveNeeded = False;
	player = gameManager.players[int(playerID)];
	successString = "Action successfully submitted!";

 	#TODO: security lol. what does that csrf token even do. also error check pls

	dataVersion = int(actionTuple["playerDataVersion"]);
	if dataVersion != player.playerDataVersion:
		return [True, "Your player game data is out of date. Please refresh the page and try again.", gameManager]

	# playing cards
	if (gameManager.doesPlayerNeedToPlayCard(playerID)):
		if "optionCard" not in actionTuple:
			return [True, "Please select a card to play!", gameManager];
		if "optionTarget" not in actionTuple:
			return [True, "Please select a target competitor card", gameManager];	

		currentMatch = gameManager.getCurrentMatch();
	
		competitorId = actionTuple["optionTarget"];
		for action in currentMatch.playerPendingActions:
			if action[0] == playerID:
				return [True, "You have already submitted an action for this round.", gameManager];	

		cardIdPlayed = gameManager.players[playerID].hand[actionTuple["optionCard"]];

		if (cardIdPlayed == SUPPORTER_CARD_ID):
			index = 0;
			# only one player can back each competitor
			while index < len(gameManager.players):
				if (currentMatch.playerSupported[index] == competitorId):
					return [True, "You cannot support someone who is already supported!", gameManager];	
				index += 1;

		newAction = [playerID, actionTuple["optionCard"], competitorId];
		currentMatch.playerPendingActions.append(newAction);

		if actionTuple["optionTarget"] >= 100:
			successString = "Successfully joined the crowd"
		else:
			cardPlayed = player.hand[actionTuple["optionCard"]];
			successString = "Successfully played a card on competitor #" + str(competitorId+1);

		saveNeeded = True;

	elif (gameManager.doesPlayerHaveToDraftCard(playerID)): # todo: technically this is bad
		if "optionRemoveCard" not in actionTuple:
			return [True, "Please select a card to remove!", gameManager];	
		if "optionAddCard" not in actionTuple and actionTuple["optionRemoveCard"] != 100:
			return [True, "Please select a card to add!", gameManager];

		addedCard = 100;
		if "optionAddCard" in actionTuple:
			addedCard = actionTuple["optionAddCard"];

		removedCard = actionTuple["optionRemoveCard"];

		if (removedCard == 100):
			addedCard = 100;

		player.playerCardsAddedToHand.append(addedCard);
		player.playerCardsRemovedFromHand.append(removedCard);
		gameManager.players[int(playerID)] = player;

		saveNeeded = True;

	else :
		return [False, "You have already prepared your action for this turn!", gameManager];

	if saveNeeded:
		player.playerDataVersion += 1;
		gameManager.gameSaveNeeded = True;

	return [False, successString, gameManager];

def loadGameWithIdAndPlayer(game_id, player_id):
	matchingGameDatas = GameData.objects.filter(id=game_id);
	if (len(matchingGameDatas) != 1):
		raise Http404(str(len(matchingGameDatas)) + " games with id " + str(game_id) + " found, expected 1");
	if (matchingGameDatas[0].isGameDataPlayable() == False):
		raise Http404("Game id " + str(game_id) + " is not playable");
	
	gameManager = GameManager();
	gameManager.setup(player_id, matchingGameDatas[0], "");
	gameManager.currentGameId = game_id;
	return gameManager;

def performAIActions(gameManager):
	actionsPerformed = False;

	if (gameManager.isGameOver()):
		return [actionsPerformed, gameManager];

	playerNumber = 0;
	while playerNumber < len(gameManager.players):
		thisPlayer = gameManager.players[playerNumber];
		playerAiModel = None;

		if thisPlayer.aiModel == 0:
			playerAiModel = DefaultAiModel(gameManager, playerNumber); 

		if playerAiModel:
			if (gameManager.doesPlayerNeedToPlayCard(playerNumber)):
				notificationTextTuple = processPlayerAction(playerAiModel.getChosenPlayCard(), gameManager, playerNumber);
				gameManager = notificationTextTuple[2];
				actionsPerformed = True;
			if (gameManager.doesPlayerHaveToDraftCard(playerNumber)):
				notificationTextTuple = processPlayerAction(playerAiModel.getChosenDraftCard(), gameManager, playerNumber);
				gameManager = notificationTextTuple[2];
				actionsPerformed = True;

		playerNumber += 1;

	return [actionsPerformed, gameManager];

def index(request, game_id, player_id, player_passcode, notificationText=""): # notification text is for like, errors or submission info
	gameManager = loadGameWithIdAndPlayer(game_id, player_id);
	gameManager.doFirstTimeGameSetupIfNeeded();
	gameManager.reloadUIVariables();
	
	if (gameManager.activePlayer.passcode != player_passcode):
		return HttpResponse("Invalid passcode entered for player!");
		
	if request and request.method == 'POST':
		notificationTextTuple = processPostedAction(request, gameManager, int(player_id) - 1);
		gameManager = notificationTextTuple[2];
		gameManager.reloadUIVariables();
		notificationText = notificationTextTuple[1];

	if (gameManager.activePlayer.passcode != player_passcode):
		return HttpResponse("Invalid passcode entered for player!");

	aiResultTuple = performAIActions(gameManager);
	gameManager = aiResultTuple[1];

	shouldUpdateState = gameManager.advanceGameStateIfPossible() or aiResultTuple[0];
	while shouldUpdateState == True: # keep checking as long as state changes or AI does something
		aiResultTuple = performAIActions(gameManager);
		gameManager = aiResultTuple[1];

		shouldUpdateState = gameManager.advanceGameStateIfPossible() or aiResultTuple[0];

	gameManager.reloadUIVariables();

	if gameManager.gameSaveNeeded:
		gameManager.saveGame();

	fileToRender = "renderGame.html";

	if len(notificationText) == 0:
		if (gameManager.doesPlayerNeedToPlayCard(gameManager.selectedPlayerId)):
			notificationText = "Please select a card to play.";
		elif (gameManager.UIactivePlayerMustDraftCard):
			notificationText = "Please select a card to draft.";
		elif (gameManager.UIdraftingCards):
			notificationText = "Waiting for others to draft cards...";
		else:
			notificationText = "Waiting for others to play cards..."; 
	if (gameManager.isGameOver()):
		notificationText = "The game is over! Thanks for playing.";

	gameManager.notificationText = notificationText;

	return render(request, fileToRender, {'gameManager': gameManager, 'lobbyURL' : SITE_ROOT, 'savedInputInfo' : [] });

def simulateGameCall(game_id, player_id, player_passcode):
	index(None, game_id, player_id, player_passcode);