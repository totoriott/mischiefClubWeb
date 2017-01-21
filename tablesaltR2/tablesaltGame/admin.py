from django.contrib import admin
from tablesaltGame.models import *

from createNewGame import createANewGame

# Register your models here.

def enableCards(modeladmin, request, queryset):
	queryset.update(enabled=True);
enableCards.short_description = "Enable selected";

def disableCards(modeladmin, request, queryset):
	queryset.update(enabled=False);
disableCards.short_description = "Disable selected";

def duplicateThing(modeladmin, request, queryset):
    for object in queryset:
        object.id = None
        object.save()
duplicateThing.short_description = "Duplicate selected "

def enablePublic(modeladmin, request, queryset):
	queryset.update(public=True);
enablePublic.short_description = "Mark games as public";

def disablePublic(modeladmin, request, queryset):
	queryset.update(public=False);
disablePublic.short_description = "Mark games as private";

def createANewGameAdmin(modeladmin, request, queryset):
	index = 0;
	while index < 1:
		createANewGame(None, ["[Join Now]", "[Join Now]", "[Join Now]", "[Join Now]"], True);
		index += 1;
createANewGameAdmin.short_description = "Create a public 4-player game";

def createANewSoloGameAdmin(modeladmin, request, queryset):
	index = 0;
	while index < 1:
		createANewGame(None, ["[Join Now]"], True);
		index += 1;
createANewSoloGameAdmin.short_description = "Create a public 1-player game";

def createANewSoloWithAIGameAdmin(modeladmin, request, queryset):
	index = 0;
	while index < 1:
		createANewGame(None, ["[Join Now]", "[AI-ROBOT]", "[AI-ROBOT]", "[AI-ROBOT]"], True);
		index += 1;
createANewSoloWithAIGameAdmin.short_description = "Create a public 1-player with AI game";

def createANewPrivateGameAdmin(modeladmin, request, queryset):
	index = 0;
	while index < 1:
		createANewGame(None, ["[Join Now]", "[Join Now]", "[Join Now]", "[Join Now]"], False);
		index += 1;
createANewPrivateGameAdmin.short_description = "Create a private 4-player game";

class GameConfigurationAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'enabled', 'numberOfPlayers', 'numberOfMatches', 'handSize', 'betTrackValues', 'randomizerValues'];
	actions = [enableCards, disableCards, duplicateThing];

class CompetitorCardAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'shortName', 'enabled', 'cheerTrackValues', 'abilityRangeString'];
	actions = [enableCards, disableCards];

class BoostCardAdmin(admin.ModelAdmin):
	list_display = ['id', 'name', 'enabled', 'copiesOfCard', 'advancedCard', 'abilityType', 'cheerAmount', 'betAmount', 'textDescription'];
	actions = [enableCards, disableCards];

class GameDataAdmin(admin.ModelAdmin):
	list_display = ['id', 'public', 'dataVersion', 'passcode', 'creationTime', 'notes']
	actions = [createANewGameAdmin, createANewPrivateGameAdmin, createANewSoloGameAdmin, createANewSoloWithAIGameAdmin, enablePublic, disablePublic, duplicateThing];

admin.site.register(GameConfiguration, GameConfigurationAdmin);
admin.site.register(CompetitorCard, CompetitorCardAdmin);
admin.site.register(BoostCard, BoostCardAdmin);
admin.site.register(GameData, GameDataAdmin);