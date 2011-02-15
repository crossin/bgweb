# coding=utf-8
from django.core.management.base import BaseCommand
from django.core.management.color import no_style
from optparse import make_option
import sys
import os
import datetime;

from ragendja.dbutils       import *;
from content.models         import *;
from pageharvest.settings   import *;
#filter(lambda x: x.n == 5, myList)


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-u', '--update',   dest='update_school', 
             help='update specified bbs parse config'),
        make_option( '-d', '--delete',   dest='delete_school', 
             help='clear specified bbs parse config'),
        make_option( '-a', '--add',   dest='add_school', 
             help='add specified bbs parse config'),
    )


    def handle(self,  **options):
        if options.get('update_school'):
            bn = options.get('update_school');
            try:
                ss = get_object(Schoolbbs, 'bbsname =', bn );
                cc = get_object(ParseConfig, 'school =', ss );
                c  = filter( lambda x: x['bbsname'] == bn , bbs_setting_list);
                if len(c)>0 : c = c[0];
                #for property in c: cc[property] = c[property];
                for property in c: setattr(cc,  property, c[property] );
                cc.put();
            except Exception,e:
                print 'Getting bbs parse config with name %s failed'%(bn);
                print e;
                return;
            print 'config updated successfully updated';
        if options.get('delete_school'):
            bn = options.get('delete_school');
            try:
                ss = get_object(Schoolbbs, 'bbsname =', bn );
                cc = get_object(ParseConfig, 'school =', ss );
            except Exception,e:
                print 'Getting bbs parse config with name %s failed'%(bn);
                print e;
                return;
            cc.delete();
            print 'config delete successfully removed';
        if options.get('add_school'):
            bn = options.get('add_school');
        #try:
            ss = get_object(Schoolbbs, 'bbsname =', bn );
            cc = get_object(ParseConfig, 'school =', ss );
        #except Exception,e:
            c  = filter( lambda x: x['bbsname'] == bn , bbs_setting_list);
            if len(c)>0 : c = c[0];
            config = db_create( ParseConfig,  school = ss, **c );
            print 'config successfully added';
            return;
            
            

        
        
        
            

 
