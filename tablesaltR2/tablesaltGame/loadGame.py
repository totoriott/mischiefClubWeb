from django.http import HttpResponse, Http404
from copy import deepcopy
from ast import literal_eval;
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

import random;
from createNewGame import createANewGame
from tablesaltGame.models import *
from siteConstants import *

def loadGame_getPlayableDatas():
	gameDatas = GameData.objects.filter(public=True);
	gameDatas = [x for x in gameDatas if x.isGameDataPlayable()];
	gameDatas = [x for x in gameDatas if x.isGameNotOver()];

	''' TODO: fix how filtering empty games is broken
	emptyGames = [x for x in gameDatas if x.isGameEmpty()];
	gameDatas = [x for x in gameDatas if x.isGameEmpty() == False];

	emptyGamesAdded = 0;
	while emptyGamesAdded < 3 and len(emptyGames) > emptyGamesAdded: # only show 3 completely empty games, if we have < 5 active games
		if len(emptyGames) > emptyGamesAdded and len(gameDatas) <= 5: 
			gameDatas.append(emptyGames[emptyGamesAdded]);
			emptyGamesAdded += 1;
	'''

	gameDatas.reverse();
	return gameDatas;
	
def loadGame_gameExistsWithId(game_id):
	matchingGameDatas = GameData.objects.filter(id=game_id);
	if (len(matchingGameDatas) != 1):
		return False;

	return True;

# returns [success, gameData] or [failure, error message];	
def loadGame_getGameData(game_id, player_id, pPasscode):
	if loadGame_gameExistsWithId(game_id) == False:
		return [False, "No game found with ID " + str(game_id) + "!"];
	
	matchingGameDatas = GameData.objects.filter(id=game_id);
	gameData = matchingGameDatas[0];

	# TODO: hotfix to prevent you from joining hidden games
	if gameData.isGameEmpty():
		publicGameList = loadGame_getPlayableDatas();
		gameFound = False;
		for game in publicGameList:
			if game.id == gameData.id:
				gameFound = True;
		if gameFound == False:
			return [False, "No game found with ID " + str(game_id) + "!"];	
	
	if (gameData.isGameDataPlayable() == False):
		return [False, "No game found with ID " + str(game_id) + "!"];	

	players = gameData.deserializePlayers();
	minPlayer = 1;
	maxPlayer = len(players);
	if (player_id < minPlayer or player_id > maxPlayer): 
		return [False, "Please enter a player ID between " + str(minPlayer) + " and " + str(maxPlayer) + "!"];
		
	if (len(pPasscode) != 4 or pPasscode.isdigit() == False):
		return [False, "Please enter a four digit passcode."];
		
	if (len(players[player_id - 1].passcode) > 0 and pPasscode != players[player_id - 1].passcode):
		return [False, "Incorrect passcode entered."];

	return [True, gameData]; # TODO: make it so you don't pass passcode in URL