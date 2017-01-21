from django.http import HttpResponse, Http404
from copy import deepcopy
from ast import literal_eval;
from django.shortcuts import render, redirect

import random;
from createNewGame import createANewGame
from tablesaltGame.models import *
from siteConstants import *

def index(request):
	return render(request, 'tutorial.html', { 'lobbyURL' : SITE_ROOT });