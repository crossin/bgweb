# -*- coding: utf-8 -*-
from django.db import models
from django.core.urlresolvers import reverse
from settings import *;
import re,pickle;


STATUS_NORMAL = 1;
STATUS_UNREACHABLE = 2;
STATUS_EXCEPTION = 3;

class SBPC(models.Model):#SCHOOL BBS PARSE CONFIG
    bbsname         = models.CharField( max_length=75 default = "" );
    schoolname      = models.CharField( max_length=75 default = "" );
    chinesename     = models.CharField( max_length=75 default = "" );
    rank            = models.IntegerField( default = 0 );
    lastfresh       = models.DateTimeField( null=True );
    totalparse      = models.IntegerField( default = 0 );
    failedparse     = models.IntegerField( default = 0 );
    totalparsetime  = models.FloatField( default = 0 );
    status          = models.IntegerField( default = 0 );
    parseconfig     = models.TextField( null=True );
 
class Bbslinks(models.Model):
    
    board           = models.CharField( max_length=750 default = "" );
    title           = models.CharField( max_length=750 default = "" );
    titlelink       = models.CharField( max_length=750 default = "" );
    author          = models.CharField( max_length=75  default = "" );
    visitcount      = db.IntegerProperty( default=0 );
    school          = models.ForeignKey(SBPC);
    createtime      = models.DateTimeField( auto_now=True, required = True);
    updatetime      = models.DateTimeField( auto_now=True, required = True);
    
    def get_mblog_str(self):
        link_pattern =  ROOT_URL + reverse('content_framed_detail') + '?linkid=%s';
        msg = "[%s] %s %s" %(self.school.chinesename, self.title, link_pattern %(self.id) );
        if self.author != "": msg+= " BY "+self.author;
        return msg;

        
from google.appengine.ext import db
class OptionSet(models.Model):
	name    =   db.StringProperty()
	value   =   db.TextProperty()

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
    
    







