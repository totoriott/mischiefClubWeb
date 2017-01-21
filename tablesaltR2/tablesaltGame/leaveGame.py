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
from tablesaltGame.aiModels import *
from loadGame import loadGame_getGameData

# returns [success, http response to redirect] or [failure, error message];	
COMMAND_LEAVEGAME = 0;
COMMAND_TOGGLEAI = 1;
def modifyGameWithName(game_id, player_id, pPasscode, command):
	gameLoadStatus = loadGame_getGameData(game_id, player_id, pPasscode);
	if gameLoadStatus[0] == False: # error occurred
		return gameLoadStatus;
	gameData = gameLoadStatus[1];
	players = gameData.deserializePlayers();
		
	if (command == COMMAND_LEAVEGAME): 
		# blank passcode and name so new players can join
		players[player_id - 1].playerName = "[Join Now]"
		players[player_id - 1].passcode = ""; 
		gameData.serializeAndSetPlayers(players);
		gameData.save();
		return [True, redirect(SITE_ROOT)]; 

	elif (command == COMMAND_TOGGLEAI): 
		if players[player_id - 1].aiModel >= 0:
			players[player_id - 1].aiModel = -1;
		else:
			aiClass = DefaultAiModel(None, 0);
			newAi = aiClass.getRandomAiModelWithName();
			players[player_id - 1].aiModel = newAi[0];
			players[player_id - 1].playerName = newAi[1];

		gameData.serializeAndSetPlayers(players);
		gameData.save();
		return [True, redirect(SITE_ROOT + str(game_id) + "/p" + str(player_id) + "/" + str(pPasscode))]; 	
	
	return [True, redirect(SITE_ROOT)]; 	

def index(request, game_id, player_id, player_passcode):
	successTuple = modifyGameWithName(int(game_id), int(player_id), player_passcode, COMMAND_LEAVEGAME);
			
	if successTuple[0] == True:
		return successTuple[1];

	return HttpResponse(successTuple[1]); # some error happened

def toggleAi(request, game_id, player_id, player_passcode):
	successTuple = modifyGameWithName(int(game_id), int(player_id), player_passcode, COMMAND_TOGGLEAI);
			
	if successTuple[0] == True:
		return successTuple[1];

	return HttpResponse("ok");#successTuple[1]); # some error happened