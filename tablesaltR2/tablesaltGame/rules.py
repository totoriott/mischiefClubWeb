from django.http import HttpResponse, Http404
from copy import deepcopy
from ast import literal_eval;
from django.shortcuts import render, redirect

import random;
from createNewGame import createANewGame
from tablesaltGame.models import *
from siteConstants import *

def r2_rules(request):
	allBoostCards = BoostCard.objects.all();
	allCompetitorCards = CompetitorCard.objects.all();

	return render(request, 'r2_rules.html', { 'lobbyURL' : SITE_ROOT, 'allBoostCards': allBoostCards, 'allCompetitorCards': allCompetitorCards });