"""
A management command which deletes expired accounts (e.g.,
accounts which signed up but never activated) from the database.

Calls ``RegistrationProfile.objects.delete_expired_users()``, which
contains the actual logic for determining which accounts are deleted.

"""

from django.core.management.base import BaseCommand
from optparse import make_option
from ragendja.dbutils            import *;

from content.models         import *;
from pageharvest.settings   import *;

import datetime;


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option( '-l', '--listfailed',  dest='listfailed', 
             help='list school with error status'),
        make_option( '-m', '--marknormal',  dest='marknormal', 
             help='mark innormal school into normal'),
        make_option( '-d', '--deleteschoollink',  dest='deletelink', 
             help='deletelinksofsomeschool'),
    )


    def handle(self,  **options):
        
        if options.get('listfailed'):
            def getnameforstatus(status):
                namelist = ['base','normal','innormal','structure problem'];
                return namelist[status];
        
            failed = ParseConfig.all().filter( 'status >', 1 ).fetch(100);
            print 'listing school parse config with innormal status ';
            for pc in failed:
                print "school %s ,bbs name: %s, with status %s" %( pc.school.chinesename, pc.school.bbsname, getnameforstatus(pc.status) );
                
            
            
        if options.get('marknormal'):
            schoolname = options.get('marknormal');
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
            pc.status = 1;
            pc.put();
            print 'school back into normal now';
        if options.get('deletelink'):
            schoolname = options.get('deletelink');
            qschool = Schoolbbs.all().filter( 'bbsname =', schoolname);
            if( qschool.count() == 0 ):
                print 'no school of that name';
                return;
            school = qschool.fetch(1)[0];
            qlinks = Bbslinks.all().filter( 'school =', school );
            if( qlinks.count() == 0 ):
                print 'no links of that school';
                return;
            link_count = qlinks.count();
            print 'find %d links'%link_count;
            links = qlinks.fetch(link_count);
            for link in links:
                link.delete();
            
            print '%d links from that school deleted'%link_count;
            

                                                
           
        
