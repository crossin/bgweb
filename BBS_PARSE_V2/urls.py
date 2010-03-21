# -*- coding: utf-8 -*-
from django.conf.urls.defaults import *
from ragendja.urlsauto  import urlpatterns
from ragendja.auth.urls import urlpatterns as auth_patterns
#from myapp.forms import UserRegistrationForm
from django.contrib import admin

admin.autodiscover()
from views import *;

handler500 = 'ragendja.views.server_error'

urlpatterns =  patterns('',
    (r'^$', index),
    # url(r'^$', direct_to_template, {'template': 'main.html'}, name='index'),
    #(r'^admin/(.*)', admin.site.root),
    (r'^content/', include('content.urls')),
    url(r'^gaebar/', include('gaebar.urls')),

) +auth_patterns+ urlpatterns

