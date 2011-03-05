# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto  import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
#admin.autodiscover()
from views import *;
from content.views import viewframedcontentV2 as golink;
from content.views import viewbyschool as index;

urlpatterns =  patterns('',
    #(r'^$', index),
    url(r'^$$', index,  {'template': 'content_by_school.html'},     name='home'),
    # url(r'^$', direct_to_template, {'template': 'main.html'}, name='index'),
    #(r'^admin/(.*)', admin.site.root),
    (r'^content/', include('content.urls')),
    (r'^ad/',      include('adsys.urls')),
    url(r'^go$',golink, {'template':'framed_link_content.html'},    name='golink'),
) +auth_patterns+ urlpatterns

