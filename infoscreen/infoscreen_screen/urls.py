# django imports
from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('infoscreen.infoscreen_screen.views',
    url(r'^$', 'index', name='index'),
)

