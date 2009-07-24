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


def respond(request, template, params=None):
  if params is None:
    params = {}   
  if not template.endswith('.html'):
    template += '.html'
  return shortcuts.render_to_response(template, params)
  
def freshMostTopTen(): 
#    bbslist = [];
#    highschoolbbslist = TopTenItem.all();
#    highschoolbbslist.order('-postcount');
#    bstlen = 0;
#    if  highschoolbbslist.count() < 10 :
#        bstlen = len(highschoolbbslist);
#    else :
#        bstlen = 10;
#       
#    results = highschoolbbslist.fetch(bstlen);
#    MostTopTenItem.putStaticalResult(results);
    bbslist = [];
    highschoolbbslist = HighSchoolBbs.all();
    highschoolbbslist.order('rank');
    highschoollist1 = highschoolbbslist[0:10]
    for school in  highschoollist1:
        toptenlist = TopTenItem.gql('where school = :1 ORDER BY order ASC', school);

        bbsinfo = {
                    'name': unicode(school.schoolname),
                    'schoolchinesename':unicode(school.schoolchinesename),
                    'chinesename':unicode(school.chinesename),
                    'itemlist':toptenlist,
                    }
        bbslist.append(bbsinfo);
    recolist = [];
    for list in bbslist:
        recoinfo = list['itemlist'][0];
#        recoinfo = {
#                    'boardlink': list['itemlist'][0].boardlink,
#                    'board': list['itemlist'][0].board,
#                    'titlelink': list['itemlist'][0].titlelink,
#                    'title': list['itemlist'][0].title,
#        }
        recolist.append(recoinfo);
    MostTopTenItem.putStaticalResult(recolist);
    return  recolist;
    

def freshbbs2():  
    b = BBSParser();
    needRegularExpressionList2 = [newsmth, zjubbs, lilybbs, fudanbbs, ustcbbs, sysubbs, whubbs, xjtubbs, scubbs, hitbbs];
    #needRegularExpressionList2 = [newsmth, zjubbs, lilybbs, fudanbbs, ustcbbs, sysubbs, whubbs, xjtubbs, scubbs, hitbbs, tjubbs, csubbs, buaabbs, dlutbbs, njuptbbs, bjtubbs, tjbbs];
    context = [];
    for bbs in needRegularExpressionList2:
        context.append(b.parsebbsbyRegularExpression(bbs));

    for bbsinfoitem in context:
        HighSchoolBbs.PutBbsInfo(bbsinfoitem);
    

    return context;

def freshbbs():  
    b = BBSParser();
    needXpathBBSList = [ sjtubbs , jlubbs, xmubbs , sdubbs, seubbs, rucbbs, lzubbs, caubbs ];
    #needXpathBBSList = [ sjtubbs , jlubbs, xmubbs , sdubbs, seubbs, rucbbs, lzubbs, caubbs, ustbbbs, uestcbbs ];
#    needRegularExpressionList1 = []; 
#    needRegularExpressionList2 = [ustcbbs, zsubbs, whubbs, xjtubbs, scubbs, hitbbs, tjubbs, csubbs, buaabbs, dlutbbs, njuptbbs, bjtubbs, tjbbs];

    context = [];

#    for bbs in needRegularExpressionList1:
#        context.append(b.parsebbsbyRegularExpression(bbs));
    for bbs in needXpathBBSList:
        context.append(b.parsebbsbyXpath(bbs));
  
    for bbsinfoitem in context:
        HighSchoolBbs.PutBbsInfo(bbsinfoitem);
    
    return context;

def freshbbs3():  
    b = BBSParser();
    needRegularExpressionList3 = [ tjubbs, csubbs, buaabbs, dlutbbs, njuptbbs, bjtubbs, tjbbs];
    needXpathBBSList = [ ustbbbs, uestcbbs];
    context = [];
    for bbs in needRegularExpressionList3:
        context.append(b.parsebbsbyRegularExpression(bbs));
    for bbs in needXpathBBSList:
        context.append(b.parsebbsbyXpath(bbs));

    for bbsinfoitem in context:
        HighSchoolBbs.PutBbsInfo(bbsinfoitem);
    
    freshMostTopTen();
    return context; 

def getFreshBBS2(request): 
    freshbbs2();
    return HttpResponse("Part2 Updated Successfully")   
    
def getFreshBBS1(request):
    freshbbs();
    return HttpResponse("Part1 Updated Successfully")
    
def getFreshBBS3(request):
    freshbbs3();
    return HttpResponse("Part3 Updated Successfully")
    

def getbbsitemlist(bbsname):
    slist = HighSchoolBbs.gql('where schoolname = :1', bbsname);
    if slist.count() == 0 :
        return;
    school = slist[0];
    toptenlist = TopTenItem.gql('where school = :1 ORDER BY order ASC', school);
    bbsinfo = {
                'name': unicode(school.schoolname),
                'schoolchinesename':unicode(school.schoolchinesename),
                'chinesename':unicode(school.chinesename),
                'itemlist':toptenlist,
    }
    return bbsinfo;
    

def getbbs(request):
#    bbsnamelist = ['sjtu', 'smth2', 'zju', 'lily', 'fudan', 'ustc', 'zsu', 'whu', 'jlu', 'xjtu', 'scu', 'hit', 'sdu', 'tongji', 'csu', 'seu', 'ruc', 'buaa', 'xmu', 'dlut' ];
    bbsnamelist = [];
    highschoollist = HighSchoolBbs.all();
    count = highschoollist.count();
    highschoollist.order('rank');
    for item in highschoollist:
        bbsnamelist.append(item.schoolname);
    if 'selectedtop1' in request.COOKIES and request.COOKIES['selectedtop1']:
        favbbs = request.COOKIES['selectedtop1'];
        try:
            i = bbsnamelist.index(favbbs)
            bbsnamelist.remove(favbbs)
            bbsnamelist.insert(0, favbbs);
        except ValueError:
            bbsnamelist.insert(0, favbbs);
            bbsnamelist.pop();
    bbslist = [];
    
    for name in  bbsnamelist:
        bbslist.append(getbbsitemlist(name));
    if  count >= 20:
        cardlist = bbslist[0:20];
    else:
         cardlist = bbslist;
    if  ('card' in request.GET) : 
        return render_to_response('list_card.html', {'context':cardlist});
    bbstoplist = bbslist[0:10];
    recolist = MostTopTenItem.all();
    return render_to_response('BBS_PARSE.html', {'context':bbstoplist, 'recommend':recolist});
    
def getbbs4xn(request):
#    bbsnamelist = ['sjtu', 'smth2', 'zju', 'lily', 'fudan', 'ustc', 'zsu', 'whu', 'jlu', 'xjtu', 'scu', 'hit', 'sdu', 'tongji', 'csu', 'seu', 'ruc', 'buaa', 'xmu', 'dlut' ];
    bbsnamelist = [];
    highschoollist = HighSchoolBbs.all();
    count = highschoollist.count();
    highschoollist.order('rank');
    for item in highschoollist:
        bbsnamelist.append(item.schoolname);
    if 'selectedtop1' in request.COOKIES and request.COOKIES['selectedtop1']:
        favbbs = request.COOKIES['selectedtop1'];
        try:
            i = bbsnamelist.index(favbbs)
            bbsnamelist.remove(favbbs)
            bbsnamelist.insert(0, favbbs);
        except ValueError:
            bbsnamelist.insert(0, favbbs);
            bbsnamelist.pop();
    bbslist = [];
    
    for name in  bbsnamelist:
        bbslist.append(getbbsitemlist(name));

    bbstoplist = bbslist[0:10];
    recolist = MostTopTenItem.all();
    return render_to_response('BBS_PARSE_4xn.html', {'context':bbstoplist, 'recommend':recolist});

#def getMostTop10(request):
#    return redirect(' /page/BbsRender.html')
    
    
def getRecommended(request):
    recolist = MostTopTenItem.all();
    return render_to_response('list_recommend.html', { "context":recolist}); 


def getfullbbslist(request):
    bbslist = [];
    highschoollist = HighSchoolBbs.all();
    count = highschoollist.count();
    highschoollist.order('rank');
    highschoollist1 = highschoollist[10:count];
    for school in  highschoollist1:
        toptenlist = TopTenItem.gql('where school = :1 ORDER BY order ASC', school);

        bbsinfo = {
                    'name': unicode(school.schoolname),
                    'schoolchinesename':unicode(school.schoolchinesename),
                    'chinesename':unicode(school.chinesename),
                    'itemlist':toptenlist,
                    }
        bbslist.append(bbsinfo);
    
    if  ('card' in request.GET) : 
       return render_to_response('list_card.html', {'context':bbslist});
    
    return render_to_response('BBS_PARSE_LIST.html', {'context':bbslist});
    
    
def get_bbsnamelist(request):
    highschoollist = HighSchoolBbs.all();
    count = highschoollist.count();
    highschoollist.order('rank');
#    total_len = highschoollist.count();
    if count >= 20:
        total_len = 20;
    else:
        total_len = count;
    unit_len = total_len / 3 + 1;
    namelist1 = highschoollist[0:unit_len];
    namelist2 = highschoollist[unit_len + 1:unit_len * 2 + 1];
    namelist3 = highschoollist[unit_len * 2 + 2:total_len];
    
    return render_to_response('list_bbs.html', {
                                        'namelist1':namelist1,
                                        'namelist2':namelist2,
                                        'namelist3':namelist3,
                                        });
    
    
        
    
                    


                            
    




