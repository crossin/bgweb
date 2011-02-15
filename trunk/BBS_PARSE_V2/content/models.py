# -*- coding: utf-8 -*-
from google.appengine.api import users
from google.appengine.ext import db
from django.core.urlresolvers import reverse
from ragendja.dbutils import *
from content import  modelutil;
from settings import *;
import re,pickle;

class Schoolbbs(db.Model):
    bbsname         = db.StringProperty(    default = "" );
    schoolname      = db.StringProperty(    default = "" );
    chinesename     = db.StringProperty(    default = "" );
    rank            = db.IntegerProperty(   default = 0  );
    lastfresh       = db.DateTimeProperty(  );

STATUS_NORMAL = 1;
STATUS_UNREACHABLE = 2;
STATUS_EXCEPTION = 3;

class ParseConfig(db.Model):
    totalparse        = db.IntegerProperty(   default = 0  );
    failedparse       = db.IntegerProperty(   default = 0  );
    totalparsetime    = db.FloatProperty( default = 0.0 );
    lastfresh         = db.DateTimeProperty(  );
    status            = db.IntegerProperty( default = 1 );
    root                = db.StringProperty(    default = "" );
    locate              = db.StringProperty(    default = "" );
    parsetype           = db.IntegerProperty(   default = 1  );
    xpath               = db.StringProperty(    default = "" );
    re_block_t          = db.StringProperty(    default = "" , multiline = True);
    re_board_t          = db.StringProperty(    default = "" );
    re_board1_t         = db.StringProperty(    default = "" );
    dom_row_pattern     = db.StringProperty(    default = "" , multiline = True);
    encoding            = db.StringProperty(    default = "" );
    comment             = db.StringProperty(    default = "" );
    rank            = db.IntegerProperty(   default = 0  );
    additional          = db.StringProperty(    default = "" ); 
    school              = db.ReferenceProperty( Schoolbbs, required=True);

    def getFaileRate(self):
        if( self.totalparse == 0 ): return 0;
        return float( self.failedparse )/float( self.totalparse );
    def getAverageParseTime(self):
        if( self.totalparse == 0 ): return 0;
        return self.totalparsetime / float(self.totalparse);
    def toDict(self):
        result = {
           'root':self.root, 'locate':self.locate, 'parsetype':self.parsetype,
           'xpath':self.xpath , 'dom_row_pattern':self.dom_row_pattern,
           'encoding':self.encoding, 'needXpath':self.parsetype==1,
           'schoolname':self.school.schoolname,
           'chinesename':self.school.chinesename,
           'bbsname':self.school.bbsname,
           #'additional':self.additional,
           #'re_block':re.compile( self.re_block_t, re.DOTALL),  
           #'re_board':re.compile( self.re_board_t, re.DOTALL),
           #'re_board1':re.compile( self.re_board1_t, re.DOTALL),
        };
        if( self.re_block_t != "" ): result['re_block'] = re.compile( self.re_block_t, re.DOTALL);
        if( self.re_board_t != "" ): result['re_board'] = re.compile( self.re_board_t, re.DOTALL);
        if( self.re_board1_t != "" ): result['re_board1'] = re.compile( self.re_board1_t, re.DOTALL);
        if( self.additional != "" ): result['additional'] = self.additional;
        return result

class MTags(db.Model):
    name            = db.StringProperty( default="" );

class Announcement( db.Model):
    content         = db.TextProperty( default="" );
    
class UserAccount(db.Model):
    email    = db.EmailProperty( required=True );
    
class Bbslinks(db.Model):
    
    unsearchable_properties = ['board','titlelink','school']
    json_does_not_include   = ['school']
    
    board           = db.StringProperty( default="" )
    title           = db.StringProperty( multiline=True , default="" )
    titlelink       = db.StringProperty( multiline=True , default="" )
    author          = db.StringProperty( default="" )
    source          = db.StringProperty( default=u"BBS" )

    commentcount    = db.IntegerProperty( default=0 );
    visitcount      = db.IntegerProperty( default=0 );
    supportcount    = db.IntegerProperty( default=0 );
    objectcount     = db.IntegerProperty( default=0 );
    collectcount    = db.IntegerProperty( default=0 );
    
    school          = db.ReferenceProperty( Schoolbbs, required=True);
    createtime      = db.DateTimeProperty( required = True);
    updatetime      = db.DateTimeProperty( required = True);
    tags             = db.StringListProperty( default = [ u'十大收录']);
    
    class Meta:
        pass;
    
    def get_mblog_str(self):
        link_pattern =  ROOT_URL + reverse('content_framed_detail') + '?linkid=%s';
        msg = "[%s] %s %s" %(self.school.chinesename, self.title, link_pattern %(self.id) );
        if self.author != "": msg+= " BY "+self.author;
        return msg;
    def contain_tag(self, tag ):
        return tag in self.tags;
    
    def get_mblog_item(self):
        item = {}
        link_pattern =  ROOT_URL + reverse('content_framed_detail') + '?linkid=%s';
        item['link'] = link_pattern %(self.id);
        item['pattern'] = "[%s] %s %s By %s";
        item['schoolname'] = self.school.chinesename;
        item['title'] = self.title;
        item['author'] = self.author;
        return item;


    """
    @property
    def school_name(self):
        return Bbslinks.school.get_value_for_datastore(self).bbsname;
    """
class LinkTags(db.Model):
    name            = db.StringProperty( default="" );
    link            = db.ReferenceProperty( Bbslinks, required=True);
    
        
class Tag(modelutil.MemcachedModel):
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
    
class Comment(modelutil.SerializableModel):
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
    
    #name        = db.StringProperty()
    #email       = db.EmailProperty()
    #homepage    = db.StringProperty()
    #title       = db.StringProperty()
    body        = db.TextProperty(required=True)
    #published   = db.DateTimeProperty(auto_now_add=True)
    link        = db.ReferenceProperty(Bbslinks)
    #thread      = db.StringProperty(required=True)

    def get_indentation(self):
        # Indentation is based on degree of nesting in "thread"
        nesting_str_array = self.thread.split('.')
        return min([len(nesting_str_array), 10])

    def next_child_thread_string(self):
        'Returns thread string for next child of this comment'
        return get_thread_string(self.link, self.thread + '.')

class BGFriendStatics(db.Model):
	abstract 		= db.TextProperty(required=True);
	type 			= db.StringProperty( required=True  );
	ip				= db.StringProperty( required=True  );
	score			= db.IntegerProperty( default=0 );

class BGFriendRank(db.Model):
	abstract 		= db.ReferenceProperty(BGFriendStatics);
	fillee			= db.StringProperty( required=True  );
	bgfriend		= db.StringProperty( required=True  );

class OptionSet(db.Model):
	name=db.StringProperty()
	value=db.TextProperty()

	@classmethod
	def getValue(cls,name,default=None):
		try:
			opt=OptionSet.get_by_key_name(name)
			return pickle.loads(str(opt.value))
		except:
			return default

	@classmethod
	def setValue(cls,name,value):
		opt=OptionSet.get_or_insert(name)
		opt.name=name
		opt.value=pickle.dumps(value)
		opt.put()

	@classmethod
	def remove(cls,name):
		opt= OptionSet.get_by_key_name(name)
		if opt:
			opt.delete()
    
    







