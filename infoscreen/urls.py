from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'infoscreen.views.home', name='home'),
    # url(r'^infoscreen/', include('infoscreen.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)


# if debug is set, serve static files
if settings.DEBUG:
    urlpatterns += patterns('django.contrib.staticfiles.views',
        url(r'^static/(?P<path>.*)$', 'serve'),
    )


# redirect to urls in the infoscreen app
urlpatterns += patterns('',
     url(r'^', include('infoscreen.infoscreen_screen.urls', namespace='screen', app_name='infoscreen_screen')),
    )
