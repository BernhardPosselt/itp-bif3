# Django imports
import threading
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from django.conf.urls.defaults import *
from infoscreen.infoscreen_screen.xml_api_query import xml_api_query


# enable admin interfaces
admin.autodiscover()
urlpatterns = patterns('',
    url(r'^admin/website/configuration/$', 'infoscreen_screen.views.views.website_settings', name='website_settings'),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)


# if debug is set, serve static files
if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()


# redirect to urls in the infoscreen app
urlpatterns += patterns('',
	url(r'^', include('infoscreen.infoscreen_screen.urls', namespace='screen', app_name='infoscreen_screen')),
)

t = threading.Thread(target=xml_api_query)
t.setDaemon(True)
t.start()
