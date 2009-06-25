from google.appengine.api import users
from google.appengine.ext import db
from google.appengine.ext.db import djangoforms

import django
from django import http
from django import shortcuts



class HighSchoolBbs(db.Model):
    schoolname      = db.StringProperty( required = True)
    chinesename     = db.StringProperty()
    rank            = db.IntegerProperty()
    @staticmethod
    def PutBbsInfo(  bbsinfo ):
        if bbsinfo is None: 
            return;
        
        config = bbsinfo['config'];
       
        qSchool = HighSchoolBbs.gql("WHERE schoolname = :1", config['name'] );
        if( qSchool.count() > 0 ):
            nschool = qSchool[0];
        else:
            nschool = HighSchoolBbs( 
                    schoolname  = unicode(config['name']), 
                    chinesename = unicode(config['chinesename']),
                    rank        = config['rank']);
            nschool.put();
    
        qTopTenItem = TopTenItem.gql('where school = :1',nschool);
        
        for item in qTopTenItem :
            item.delete();
        itemlist = bbsinfo['itemlist'];
        
        for i in range( len(itemlist) ):
            item = itemlist[i];
            Titem = TopTenItem( board       = unicode( item['board']),
                                boardlink   = unicode( item['boardlink'] ) ,
                                title       = db.Text(item['title']),
                                titlelink   = item['titlelink'],
                                author      = unicode( item['author'] ),
                                authorlink  = unicode( item['authorlink'] ),
                                postcount   = int(item['postcount']),
                                order       = i,
                                school      = nschool);
    
            Titem.put();
        
        return;


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
    
class MostTopTenItem( db.Model ):
    chinesename = db.StringProperty();
    title       = db.StringProperty( multiline=True);
    titlelink   = db.StringProperty();
    board       = db.StringProperty();
    author      = db.StringProperty();
    postcount   = db.IntegerProperty();
    
    @staticmethod
    def putStaticalResult( itemlist ):
        if itemlist is None:
            return;
        old_list = MostTopTenItem.all();
        for item in old_list :
            item.delete();
        for item in itemlist:
            n_result = MostTopTenItem(
                        chinesename = unicode(item.school.chinesename),
                        title       = item.title,
                        titlelink   = item.titlelink,
                        board       = item.board,
                        author      = item.author,
                        postcount   = item.postcount);                        
            n_result.put();
        return;
    
     
    
    
	

	







