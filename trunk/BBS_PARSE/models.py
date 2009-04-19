import os
from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

import django
from django import http
from django import shortcuts

# Create your models here.

class HighSchoolBbs(db.Model):
    schoolname      = db.StringProperty( required = True)
    chinesename     = db.StringProperty()


class TopTenItem(db.Model):
    board       = db.StringProperty()
    boardlink   = db.StringProperty()
    title       = db.StringProperty( multiline=True)
    titlelink   = db.StringProperty()
    author      = db.StringProperty()
    authorlink  = db.StringProperty()
    school      = db.ReferenceProperty(HighSchoolBbs, required = True );
    postcount   = db.IntegerProperty();
    order       = db.IntegerProperty();
	

	







