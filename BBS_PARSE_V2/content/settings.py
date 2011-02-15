# -*- coding: utf-8 -*-
from ragendja.settings_post import settings

settings.add_app_media( 'combined-content.js'           
    , 'content/bundle.js' )#function prototype  add_app_media( arg, *arglist)
settings.add_app_media( 'combined-content.css'          
    , 'content/layout.css',)
settings.add_app_media( 'content-xlayout.css'           
    , 'content/xlayout.css')

# Change your email settings
ROOT_URL = "http://127.0.0.1:8000";
from ragendja.settings_pre import *

if on_production_server:
    ROOT_URL = 'http://bbstop10.appspot.com';
else:
    ROOT_URL = "http://127.0.0.1:8000";
    
SINA_MBLOG = u'新浪微博';
N163_MBLOG = u'网易微博';
TWITTER_MBLOG = 'Twitter';

SPECIAL_TAGS = [SINA_MBLOG,N163_MBLOG,TWITTER_MBLOG];

PAGE_SIZE = 20;
PAGES_TO_LIST = 10;
USER_QUOTA = 100;