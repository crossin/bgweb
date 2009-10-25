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



class Bbslinks(search.SearchableModel):
    board           = db.StringProperty( default="" )
    title           = db.StringProperty( multiline=True , default="" )
    titlelink       = db.StringProperty( default="" )
    author          = db.StringProperty( default="" )

    commentcount    = db.IntegerProperty( default=0 );
    visitcount      = db.IntegerProperty( default=0 );
    supportcount    = db.IntegerProperty( default=0 );
    objectcount     = db.IntegerProperty( default=0 );
    collectcount    = db.IntegerProperty( default=0 );
    
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
    
class Tag(models.MemcachedModel):
    # Inserts these values into aggregate list returned by Tag.list()
    list_includes = ['counter.count', 'name']

    def delete(self):
        self.delete_counter()
        super(Tag, self).delete()

    def get_counter(self):
        counter = models.Counter('Tag' + self.name)
        return counter

    def set_counter(self, value):
        # Not implemented at this time
        pass

    def delete_counter(self):
        models.Counter('Tag' + self.name).delete()

    counter = property(get_counter, set_counter, delete_counter)

    def get_name(self):
        return self.key().name()
    name = property(get_name)
    
class Comment(models.SerializableModel):
    """Stores comments and their position in comment threads.

    Thread string describes the tree using 3 digit numbers.
    This allows lexicographical sorting to order comments
    and easy indentation computation based on the string depth.
    Example for comments that are nested except first response:
    001
      001.001
      001.002
        001.002.001
          001.002.001.001
    NOTE: This means we assume less than 999 comments in
      response to a parent comment, and we won't have
      nesting that causes our thread string > 500 bytes.
      TODO -- Put in error checks
    """
    
    name        = db.StringProperty()
    email       = db.EmailProperty()
    homepage    = db.StringProperty()
    title       = db.StringProperty()
    body        = db.TextProperty(required=True)
    published   = db.DateTimeProperty(auto_now_add=True)
    link        = db.ReferenceProperty(Bbslinks)
    thread      = db.StringProperty(required=True)

    def get_indentation(self):
        # Indentation is based on degree of nesting in "thread"
        nesting_str_array = self.thread.split('.')
        return min([len(nesting_str_array), 10])

    def next_child_thread_string(self):
        'Returns thread string for next child of this comment'
        return get_thread_string(self.link, self.thread + '.')


   
signals.pre_delete.connect(cleanup_relations, sender=Schoolbbs)


    
     
    
    
	

	







