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
    help = "Clear all the schools in the db"

    def handle_noargs(self, **options):
        def deleteallclassobjects( cls ):
            list = get_object_list( cls );
            for item in list:
                item.delete();
             
        modellist = [Schoolbbs,Bbslinks,ParseConfig,MTags,LinkTags ];
        for model in modellist:
            deleteallclassobjects( model );
        
        print 'All data cleared';
            
           
        
