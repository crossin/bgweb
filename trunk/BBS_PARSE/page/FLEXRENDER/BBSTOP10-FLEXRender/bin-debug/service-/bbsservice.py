import pyamf
from pyamf.remoting.gateway.django import DjangoGateway
from google.appengine.ext import db
from google.appengine.ext import webapp

from model.models import *;

            
            
def getBbsBlocks(request, bbslist):
    #get the most active posts
    bbslist = MostTopTenItem.all().fetch( 10 );       
    return { "selectedbbs":bbslist    }
    
    
    


    

    
    

bbsGateway = DjangoGateway({
    'bbsservice.getBbsBlocks':getBbsBlocks,
})
