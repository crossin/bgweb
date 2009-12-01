from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from optparse import make_option
import sys
import os

from ragendja.dbutils       import *;
from content.models         import Schoolbbs;
from pageharvest.settings   import *;
from pageharvest.bbs_parser import BBSParser;

import datetime;

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-c', '--schoolcount', action='store', dest='harvest_count', default=27,
            type='int', help='harvest school links of specified count'),
    )
    help = 'harvest links of All stored bbs settings'
    #args = "fixture [fixture ...]"

    def handle(self,  **options):
        parser          =   BBSParser();
        schoolcount     =   int(options.get('harvest_count'))#options.harvest_count;
        currentcount    = 0;
        
        for bbs_config in bbs_setting_list :
            parser.parsebbs( bbs_config );
            
            currentcount = currentcount + 1;
            if currentcount >= schoolcount:
                break;
        
        
            

 
