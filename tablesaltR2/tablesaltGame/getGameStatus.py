from django.http import HttpResponse, Http404

from loadGame import loadGame_getGameData

# returns gameDataVersion or error message;	
def index(request, game_id, player_id, player_passcode):
	gameLoadStatus = loadGame_getGameData(int(game_id), int(player_id), player_passcode);

	if (gameLoadStatus[0] == True): #success
		return HttpResponse(gameLoadStatus[1].dataVersion);

	return HttpResponse(gameLoadStatus[1]); # either return actual value, or error message