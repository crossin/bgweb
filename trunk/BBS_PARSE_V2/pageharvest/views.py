# -*- coding: utf-8 -*-
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from ragendja.template import render_to_response
from ragendja.dbutils  import *;

from settings import *;
from bbs_parser import BBSParser;
from content.models import *;
from datetime import *;

from pageharvest.settings   import *;

import time;

parser      =   BBSParser();





def gae_cron_job(request, '', template_name='', extra_context=None ):
    now         = datetime.now()
    delta       = timedelta( minutes = -40 );
    criteria    = now + delta;
    #school_list = get_object_list(Schoolbbs, ' lastfresh < ', criteria );
    not_updated_list  = filter( lambda x:x['lastfresh'] < criteria , bbs_setting_list );
    
    duration = 0;
    for bbs_config in not_updated_list:
        #t1 = time.time();
        parsetime = parser.parsebbs( bbs_config );
        #t2 = time.time();
        duration = duration + parsetime;
        if duration > parse_time_limit:
            return;

    