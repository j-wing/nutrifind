from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('main.views',
    # Examples:
    url(r'^$', 'index'),
    url(r'^names/$', 'names'),
    url(r'^get_ingredients/$', 'get_ingredients'),

)
