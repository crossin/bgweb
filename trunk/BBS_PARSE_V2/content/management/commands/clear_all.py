"""
A management command which deletes expired accounts (e.g.,
accounts which signed up but never activated) from the database.

Calls ``RegistrationProfile.objects.delete_expired_users()``, which
contains the actual logic for determining which accounts are deleted.

"""

from django.core.management.base import NoArgsCommand
from ragendja.dbutils            import *;

from content.models         import Schoolbbs;
from pageharvest.settings   import *;

import datetime;


class Command(NoArgsCommand):
    help = "Clear all the schools in the db"

    def handle_noargs(self, **options):
        school_list = get_object_list( Schoolbbs );
        for school in school_list :
            school.delete();
           
        
