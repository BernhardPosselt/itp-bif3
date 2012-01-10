#!/usr/bin/env python
#-*- coding:utf-8 -*-

from distutils.core import setup

setup(
    name = 'infoscreen',
	version = '1.0',
	description = 'Firefighters Infoscreen',
	author = 'Bernhard Posselt',
	author_email = 'bernhard.posselt@gmx.at',
	url = 'https://github.com/Raydiation/itp-bif3',
	packages = [
	            'infoscreen', 
	                'infoscreen/infoscreen_screen', 
	                    'infoscreen/infoscreen_screen/views', 
	                'infoscreen/inc', 
	],
	package_data = {
	    '' : [
	        'infoscreen/initial_data.json',
	        'infoscreen/infoscreen_screen/sql/*', 
	        'infoscreen/static/*', 
	            'infoscreen/static/admin/*', 
	                'infoscreen/static/admin/css/*',
	                'infoscreen/static/admin/js/*',
    	                'infoscreen/static/admin/js/admin/*',
	                'infoscreen/static/admin/img/*', 
	                    'infoscreen/static/admin/img/gis/*', 
	                    'infoscreen/static/admin/img/admin/*', 
	            'infoscreen/static/audio/*',
	            'infoscreen/static/img/*',
	            'infoscreen/static/script/*',
	                'infoscreen/static/script/lib/*',
	            'infoscreen/static/style/*',
	                'infoscreen/static/style/font/*',
	            'infoscreen/static/upload/*',
	                'infoscreen/static/upload/kml/*',
	        'infoscreen/tpl/*', 
	            'infoscreen/tpl/admin/*',
	            'infoscreen/tpl/javascript/*',
	            'infoscreen/tpl/infoscreen_screen/*',
                    'infoscreen/tpl/infoscreen_screen/ajax/*',
                    'infoscreen/tpl/infoscreen_screen/gmap/*',
                    'infoscreen/tpl/infoscreen_screen/einsatzfax/*',
	        'infoscreen/wsgi/django.wsgi',
	        'infoscreen/tests/*',
    	        'infoscreen/tests/xml/*',
	    ]
	}
)

