# coding=utf-8
import logging
import cgi

import sys

from google.appengine.ext import webapp
from django.shortcuts import *
from django.http import *


from model.models import *

from bbs_settings import *;
from bbs_parser import *;


def respond(request,  template, params=None):
  if params is None:
    params = {}   
  if not template.endswith('.html'):
    template += '.html'
  return shortcuts.render_to_response(template, params)
  
def freshMostTopTen(): 
    bbslist = [];
    highschoolbbslist = TopTenItem.all();
    highschoolbbslist.order('-postcount');
    bstlen = 0;
    if  highschoolbbslist.count() < 10 :
        bstlen = len(highschoolbbslist);
    else :
        bstlen = 10;
       
    results =  highschoolbbslist.fetch( bstlen );
    MostTopTenItem.putStaticalResult( results );
       
    
def freshbbs( ):  
    b = BBSParser();
    needXpathBBSList = [ sjtubbs , jlubbs ];
    needRegularExpressionList1 = [smthbbs, lilybbs, fudanbbs, xjtubbs, njuptbbs ,nankaibbs, newsmth]; 
    needRegularExpressionList2 = [ ustcbbs , tjbbs, zsubbs, csubbs, dlutbbs, xmubbs ];

    context = [];

    for bbs in needRegularExpressionList1:
        context.append( b.parsebbsbyRegularExpression( bbs ));
    for bbs in needXpathBBSList:
        context.append( b.parsebbsbyXpath( bbs ));
  
    for bbsinfoitem in context:
        HighSchoolBbs.PutBbsInfo(bbsinfoitem);
    
    return context;

def freshbbs2( ):  
    b = BBSParser();
    needRegularExpressionList2 = [ ustcbbs , tjbbs, nankaibbs, zsubbs, csubbs, dlutbbs, xmubbs ];
    context = [];
    for bbs in needRegularExpressionList2:
        context.append( b.parsebbsbyRegularExpression( bbs ));

    for bbsinfoitem in context:
        HighSchoolBbs.PutBbsInfo(bbsinfoitem);
    
    freshMostTopTen();
    return context;

def getFreshBBS2( request ): 
    freshbbs2();
    return HttpResponse("Part2 Updated Successfully")   
    
def getFreshBBS1( request ):
    freshbbs();
    return HttpResponse("Part1 Updated Successfully")
    

def getbbsitemlist( bbsname ):
    slist = HighSchoolBbs.gql('where schoolname = :1', bbsname);
    if slist.count() == 0 :
        return;
    school = slist[0];
    toptenlist = TopTenItem.gql('where school = :1',school);
    bbsinfo = {
                'name': unicode(school.schoolname),
                'chinesename':unicode(school.chinesename),
                'itemlist':toptenlist,
    }
    return bbsinfo;
    

def getbbs( request ):
    bbsnamelist = ['sjtu','smth2','lily','tongji','fudan','xjtu'];
    if 'selectedtop1' in request.COOKIES and request.COOKIES['selectedtop1']:
        favbbs = request.COOKIES['selectedtop1'];
        try:
            i = bbsnamelist.index(favbbs)
            bbsnamelist.remove(favbbs)
            bbsnamelist.insert(0,favbbs);
        except ValueError:
            bbsnamelist.insert(0,favbbs);
            bbsnamelist.pop();
    bbslist = [];
    
    for name in  bbsnamelist:
        bbslist.append( getbbsitemlist(name) );
        
    if  ( 'card' in request.GET ) : 
        return render_to_response('list_card.html', {'context':bbslist});
    
    return render_to_response('BBS_PARSE.html', {'context':bbslist});

def getMostTop10( request ):
    return redirect('/page/BbsRender.html')
    
    
def getRecommended( request ):
    bbslist = MostTopTenItem.all().fetch( 10 );       
    return render_to_response('list_recommend.html', { "context":bbslist}); 


def getfullbbslist( request ):
    bbslist = [];
    highschoollist = HighSchoolBbs.all();
    highschoollist.order('rank');
    for school in  highschoollist:
        toptenlist = TopTenItem.gql('where school = :1 ORDER BY order ASC',school);

        bbsinfo = {
                    'name': unicode(school.schoolname),
                    'chinesename':unicode(school.chinesename),
                    'itemlist':toptenlist,
                    }
        bbslist.append( bbsinfo);
   
    if  ( 'card' in request.GET ) : 
        return render_to_response('list_card.html', {'context':bbslist});
    
    return render_to_response('BBS_PARSE.html', {'context':bbslist});
    
    
def get_bbsnamelist( request):
    highschoollist = HighSchoolBbs.all();
    total_len =  highschoollist.count();
    unit_len  = total_len / 3 + 1;
    namelist1 = highschoollist[0:unit_len];
    namelist2 = highschoollist[unit_len+1:unit_len*2+1];
    namelist3 = highschoollist[unit_len*2+2:total_len];
    
    return render_to_response('list_bbs.html', {
                                        'namelist1':namelist1,
                                        'namelist2':namelist2,
                                        'namelist3':namelist3,
                                        });
    
    
        
    
                    


                            
    




