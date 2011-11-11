# django imports
from django.conf.urls.defaults import patterns, include, url

# normal views
urlpatterns = patterns('infoscreen.infoscreen_screen.views.views',
    url(r'^$', 'index', name='index'),
    url(r'^bildschirm/links/$', 'bildschirm_links', name='bildschirm_links'),
    url(r'^bildschirm/rechts/$', 'bildschirm_rechts', name='bildschirm_rechts'),
)

# ajax views
urlpatterns += patterns('infoscreen.infoscreen_screen.views.ajax',
    url(r'^update/$', 'update', name='update'),
    url(r'^update/einsatz/$', 'update_einsatz', name='update_einsatz'),
    url(r'^update/karte/$', 'update_karte', name='update_karte'),
    url(r'^update/news/$', 'update_news', name='update_news'),
    url(r'^update/willkommen/$', 'update_willkommen', name='update_willkommen'),
)

# pdf views
urlpatterns += patterns('infoscreen.infoscreen_screen.views.pdf',
    url(r'^einsatzfax/$', 'einsatzfax', name='einsatzfax'),
    url(r'^einsatzfax/pdf/(?P<id>\d+)/$', 'einsatzfax_pdf', name='einsatzfax_pdf'),
    url(r'^einsatzfax/pdf/ausgedruckt/(?P<id>\d+)/$', 'einsatzfax_pdf_ausgedruckt', 
        name='einsatzfax_pdf_printed'),
)
