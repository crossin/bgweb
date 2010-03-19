from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from optparse import make_option
import sys
import os

from ragendja.dbutils       import *;
from content.models         import *;
from pageharvest.settings   import *;
from pageharvest.bbs_parser import BBSParser;

import datetime;

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-c', '--schoolcount',  dest='harvest_count', 
             help='harvest school links of specified count'),
        make_option( '-s', '--schoolname',   dest='harvest_school', 
             help='harvest school links of specified school'),
    )


    def handle(self,  **options):
        parser          =   BBSParser();
        
        if options.get('harvest_count'):
            schoolcount     =   int(options.get('harvest_count'))#options.harvest_count;
            currentcount    = 0;
            st_query = ParseConfig.all();
            #st_query = ParseConfig.all().filter( ' status = ', STATUS_NORMAL );
            all_config_count = st_query.count();
            fetch_count = min( all_config_count,schoolcount);
            
            if( fetch_count == 0 ): return;
            pc_list = st_query.order('rank').fetch(fetch_count);
    
            for bbs_config in pc_list :
                parser.parsebbs( bbs_config.toDict() , bbs_config );
            
        if options.get('harvest_school'):
            schoolname = options.get('harvest_school');
            qschool = Schoolbbs.all().filter( 'bbsname =', schoolname);
            if( qschool.count() == 0 ):
                print 'no school of that name';
                return;
            school = qschool.fetch(1)[0];
            qpc = ParseConfig.all().filter( 'school =', school );
            if( qpc.count() == 0 ):
                print 'no parse config of that school';
                return;
            pc = qpc.fetch(1)[0];
            
            parser.parsebbs( pc.toDict() , pc );
            
        """
        for bbs_config in bbs_setting_list :
            parser.parsebbs( bbs_config );
            
            currentcount = currentcount + 1;
            if currentcount >= schoolcount:
                break;
"""
        
        
        
            

 
