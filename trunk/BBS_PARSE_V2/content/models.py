from google.appengine.api import users
from google.appengine.ext import db

from django.db.models import signals
from ragendja.dbutils import cleanup_relations





class Schoolbbs(db.Model):
    bbsname     = db.StringProperty(    default="" );
    schoolname  = db.StringProperty(    default="" );
    chinesename = db.StringProperty(    default="" );
    rank        = db.IntegerProperty(   default=0  );
    lastfresh   = db.DateTimeProperty(  );
    
    class Meta:
        pass;



class Bbslinks(db.Model):
    board           = db.StringProperty( default="" )
    title           = db.StringProperty( multiline=True , default="" )
    titlelink       = db.StringProperty( default="" )
    author          = db.StringProperty( default="" )

    commentcount    = db.IntegerProperty( default=0 );
    visitcount      = db.IntegerProperty( default=0 );
    supportcount    = db.IntegerProperty( default=0 );
    objectcount     = db.IntegerProperty( default=0 );
    collectcount    = db.IntegerProperty( default=0 );
    #postcount       = db.IntegerProperty( default=0 ); 
    
    school          = db.ReferenceProperty( Schoolbbs, required=True);
    createtime      = db.DateTimeProperty( required = True);
    updatetime      = db.DateTimeProperty( required = True);
    
    class Meta:
        pass;

    """
    @property
    def school_name(self):
        return Bbslinks.school.get_value_for_datastore(self).bbsname;
    """


   
signals.pre_delete.connect(cleanup_relations, sender=Schoolbbs)


    
     
    
    
	

	







