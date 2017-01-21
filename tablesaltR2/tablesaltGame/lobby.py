from django.http import HttpResponse, Http404
from copy import deepcopy
from ast import literal_eval;
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.html import escape

import random;
from createNewGame import createANewGame
from viewGame import simulateGameCall;
from tablesaltGame.models import *
from siteConstants import *
from loadGame import loadGame_getGameData, loadGame_getPlayableDatas;

# TODO: persist player name / passcode

def getPlayableFinishedDatas():
	gameDatas = GameData.objects.filter(public=True);
	gameDatas = [x for x in gameDatas if x.isGameDataPlayable()];
	gameDatas = [x for x in gameDatas if x.isGameNotOver() == False];
	gameDatas.reverse();
	return gameDatas;
	
# returns [success, http response to redirect] or [failure, error message];	
def joinGameWithName(game_id, player_id, pName, pPasscode, rPasscode):
	gameLoadStatus = loadGame_getGameData(game_id, player_id, pPasscode);
	if gameLoadStatus[0] == False: # error occurred
		return gameLoadStatus;
	gameData = gameLoadStatus[1];
	players = gameData.deserializePlayers();

	if (len(players[player_id - 1].passcode) == 0): # if no passcode yet, that's first login. replace name now
		if gameData.isGameEmpty(): # first one gets to set room password
			gameData.passcode = str(rPasscode);

		players[player_id - 1].playerName = escape(pName); # TODO: do we wanna do this here, or more lazily
		players[player_id - 1].passcode = pPasscode;
		gameData.serializeAndSetPlayers(players);

		gameData.save();
			
	return [True, redirect(SITE_ROOT + str(game_id) + "/p" + str(player_id) + "/" + str(pPasscode))]; # TODO: make it so you don't pass passcode in URL

def index(request):
	enterNotificationText = "";
	startGameNotificationText = "";

	roomId = 0;
	roomPlayer = 1;

	# TODO: lol this is lazy
	publicGameList = loadGame_getPlayableDatas();
	finishedPublicGameList = getPlayableFinishedDatas();

	if request.method == 'POST':
		playerEnterName = request.POST["playerEnterName"];
		playerEnterCode = request.POST["playerEnterCode"];
		roomEnterCode = request.POST["roomEnterCode"];
		
		if ('submitAction' in request.POST): # new game or enter game by ID
			submitAction = request.POST["submitAction"];

			if (submitAction == "Go!"): # enter game TODO: enum this?
				roomId = int(request.POST["roomId"]);
				roomPlayer = int(request.POST["roomPlayer"]);
				
				successTuple = joinGameWithName(roomId, roomPlayer, playerEnterName, playerEnterCode, roomEnterCode);
				if (successTuple[0]):
					return successTuple[1];
				else:
					enterNotificationText = successTuple[1];

		elif 'startSoloGame' in request.POST: # TODO: FAILSAFE PLEASE
			roomId = createANewGame(None, ["[Join Now]", "[AI-ROBOT]", "[AI-ROBOT]", "[AI-ROBOT]"], True);
			roomPlayer = 1;
			# this is the same join game code as before
			successTuple = joinGameWithName(roomId, roomPlayer, playerEnterName, playerEnterCode, roomEnterCode);
			if (successTuple[0]):
				return successTuple[1];
			else:
				enterNotificationText = successTuple[1];

		elif 'simulateAiGame' in request.POST: # TODO: FAILSAFE PLEASE
			gamesToSimulate = 1;
			count = 0;
			while count < gamesToSimulate:
				roomId = createANewGame(None, ["[AI-ROBOT]", "[AI-ROBOT]", "[AI-ROBOT]", "[AI-ROBOT]"], True);
				roomPlayer = 1;
				simulateGameCall(roomId, roomPlayer, "0000");

				count += 1;
			enterNotificationText = str(count) + " games simulated.";

		else:
			for postedKey in request.POST:
				if str(postedKey).startswith("submitPublicGame,"):
					joinPublicParameters = str(postedKey).split(",");
					roomId = int(joinPublicParameters[1]);
					roomPlayer = int(joinPublicParameters[2]);
					
					successTuple = joinGameWithName(roomId, roomPlayer, playerEnterName, playerEnterCode, roomEnterCode);
					if (successTuple[0]):
						return successTuple[1];
					else:
						enterNotificationText = successTuple[1];
			
	return render(request, 'lobby.html', { "finishedPublicGameList" : finishedPublicGameList, "publicGameList" : publicGameList, "enterNotificationText" : enterNotificationText, "roomId" : roomId, "roomPlayer" : roomPlayer , "startGameNotificationText" : startGameNotificationText });