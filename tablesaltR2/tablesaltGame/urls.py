from django.conf.urls import patterns, url
from django.conf import settings
from django.conf.urls.static import static

from tablesaltGame import lobby, rules, viewGame, tutorial, leaveGame, getGameStatus

urlpatterns = patterns('',
	url(r'^$', lobby.index, name='index'),
	url(r'^rules/$', rules.r2_rules, name='rules'),

	url(r'^(?P<game_id>[0-9]+)/p(?P<player_id>[0-9]+)/(?P<player_passcode>[0-9][0-9][0-9][0-9])/$', viewGame.index, name='index'), # e.g. /10/p2/[4 digit passcode]
	url(r'^(?P<game_id>[0-9]+)/p(?P<player_id>[0-9]+)/(?P<player_passcode>[0-9][0-9][0-9][0-9])/leave/$', leaveGame.index, name='index'), # e.g. /10/p2/[4 digit passcode]/leave
	url(r'^(?P<game_id>[0-9]+)/p(?P<player_id>[0-9]+)/(?P<player_passcode>[0-9][0-9][0-9][0-9])/toggleAi/$', leaveGame.toggleAi, name='index'), # e.g. /10/p2/[4 digit passcode]/leave
	url(r'^(?P<game_id>[0-9]+)/p(?P<player_id>[0-9]+)/(?P<player_passcode>[0-9][0-9][0-9][0-9])/gameStatus/$', getGameStatus.index, name='index'), 
)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)