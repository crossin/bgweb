"""
A management command which deletes expired accounts (e.g.,
accounts which signed up but never activated) from the database.

Calls ``RegistrationProfile.objects.delete_expired_users()``, which
contains the actual logic for determining which accounts are deleted.

"""

from django.core.management.base import NoArgsCommand
from user_logic.models         import *;

import datetime;
from TestDataDefinition import *;

class Command(NoArgsCommand):
    help = "Setup Initial  data into the database"

    def handle_noargs(self, **options):
        for card in card_list:
            card.save();
        for player in player_list:
            player.save();
        for auctioncenter in auctioncenter_list:
            auctioncenter.save();
        
        for ac in auctioncenter_list:
            for card in card_list:
                rpt = RepurchasePrice( card_class=card.card_class, auctioncenter = ac );
                rpt.save();
           
        
