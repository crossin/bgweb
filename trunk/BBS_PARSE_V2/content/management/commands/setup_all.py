"""
A management command which deletes expired accounts (e.g.,
accounts which signed up but never activated) from the database.

Calls ``RegistrationProfile.objects.delete_expired_users()``, which
contains the actual logic for determining which accounts are deleted.

"""

from django.core.management.base import NoArgsCommand
from ragendja.dbutils            import *;

from content.models         import *;
from pageharvest.settings   import *;

import datetime;


class Command(NoArgsCommand):
    help = "Setup Initial bbs data into the database"

    def handle_noargs(self, **options):
        for bc in bbs_setting_list :
            item = get_object(Schoolbbs,  'schoolname =',  bc['schoolname'] );
            if not item :
                now = datetime.datetime.now();
                school = db_create( Schoolbbs, lastfresh = now, **bc );
                if( bc['bbsname'] != 'recommend' ):
                    config = db_create( ParseConfig,  school = school, **bc );
                
        print 'All School data setup successfully';
           
        
