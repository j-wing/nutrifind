from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('main.urls')),
    # url(r'^blog/', include('blog.urls')),

)
