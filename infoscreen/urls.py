# Django imports
from django.conf.urls.defaults import patterns, include, url
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin


# enable admin interfaces
admin.autodiscover()
urlpatterns = patterns('',
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
