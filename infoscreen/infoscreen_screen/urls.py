# django imports
from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template

# normal views
urlpatterns = patterns('infoscreen.infoscreen_screen.views.views',
    url(r'^$', 'index', name='index'),
    url(r'^bildschirm/frieden/links/$', 'bildschirm_frieden_links', name='bildschirm_frieden_links'),
    url(r'^bildschirm/frieden/rechts/$', 'bildschirm_frieden_rechts', name='bildschirm_frieden_rechts'),
    url(r'^bildschirm/einsatz/links/$', 'bildschirm_einsatz_links', name='bildschirm_einsatz_links'),
    url(r'^bildschirm/einsatz/rechts/$', 'bildschirm_einsatz_rechts', name='bildschirm_einsatz_rechts'),
    
    # javascript
    url(r'javascript/(?P<src>\w+)/$', 'javascript', name='javascript'),
    url(r'javascript/main/(?P<screen>\d+)/(?P<mission>\d+)/$', 'javascript_main', name='javascript_main'),
)

# ajax views
urlpatterns += patterns('infoscreen.infoscreen_screen.views.ajax',
    url(r'^ajax/update/$', 'update', name='update'),
    url(r'^ajax/update/welcome/$', 'update_welcome', name='update_welcome'),
    url(r'^ajax/update/news/$', 'update_news', name='update_news'),
    url(r'^ajax/update/vehicles/$', 'update_vehicles', name='update_vehicles'),
    url(r'^ajax/update/utils/$', 'update_utils', name='update_utils'),
    url(r'^ajax/update/vehicle/order/$', 'update_vehicle_order', name='update_vehicle_order'),
    url(r'^ajax/update/mission/$', 'update_mission', name='update_mission'),
    url(r'^ajax/update/dispos/$', 'update_dispos', name='update_dispos'),
    url(r'^ajax/update/map/$', 'update_map', name='update_map'),
)

# pdf views
urlpatterns += patterns('infoscreen.infoscreen_screen.views.pdf',
    url(r'^einsatzfax/$', 'einsatzfax', name='einsatzfax'),
    url(r'^einsatzfax/pdf/(?P<id>\d+)/$', 'einsatzfax_pdf', name='einsatzfax_pdf'),
    url(r'^einsatzfax/pdf/ausgedruckt/(?P<id>\d+)/$', 'einsatzfax_pdf_ausgedruckt', 
        name='einsatzfax_pdf_printed'),
)

#gmap view
urlpatterns += patterns('infoscreen.infoscreen_screen.views.gmap',
    url(r'^gmap/(?P<id>\d+)/$', 'gmap', name='gmap'),
    url(r'^gmap_adresse/(?P<id>\d+)/$', 'gmap_adresse', name='gmap_adresse'),
)

