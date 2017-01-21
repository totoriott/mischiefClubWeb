from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tablesalt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^', include('tablesaltGame.urls')), # main level is just the game now
    url(r'^bartender/', include(admin.site.urls)), 
)
