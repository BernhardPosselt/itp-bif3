# django imports
from django.conf.urls.defaults import patterns, include, url

# normal views
urlpatterns = patterns('infoscreen.infoscreen_screen.views.views',
    url(r'^$', 'index', name='index'),
    url(r'^news/$', 'news', name='news'),
    url(r'^willkommen/$', 'willkommen', name='willkommen'),
    url(r'^alarm/$', 'alarm', name='alarm'),
    url(r'^karte/$', 'karte', name='karte'),
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
    url(r'^einsatzfax/pdf/printed/(?P<id>\d+)/$', 'einsatzfax_pdf_printed', 
        name='einsatzfax_pdf_printed'),
)
