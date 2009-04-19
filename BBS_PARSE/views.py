# coding=utf-8
import logging
import cgi
import urllib2
import string
import sys

from google.appengine.ext import webapp
from google.appengine.api import urlfetch
from django.shortcuts import *


from django.http import *

from BeautifulSoup import BeautifulSoup;
from bsoupxpath    import Path;

from models import *


def respond(request,  template, params=None):
  if params is None:
    params = {}
    
  if not template.endswith('.html'):
    template += '.html'
  return shortcuts.render_to_response(template, params)
  

    
def testcron(request):
    #print 'cron triggered';
     logging.info('cron triggered');

    
   

def convertdom2string( domlist ):
    list_str = u'';
    
    for i in range( len(domlist) ):
        list_str += unicode(domlist[i]);
        
    return list_str;

def parse_subdom_item( subdom, config):
    parsed_result = [];
    trlist = subdom.findAll(config['lineindicator']); 
    if ( config['skiphead'] ): 
        start_index = 1;
    else:
        start_index = 0;

    
    itr_len = len(trlist) - start_index;
    if config['skiptail'] :
        itr_len = itr_len - 1;
        
    for i in range( 10 ):
        item = {
            'board':    '',
            'boardlink':'',
            'title':    '',
            'titlelink':'',
            'author':   '',
            'authorlink':'',
            'postcount':'',
        };
        
        dom_row = trlist[start_index + i];
        #print 'dom_row:',dom_row;
        
        alist = dom_row.findAll('a');
        item['board']       = unicode( alist[0].contents[0]             );
        item['boardlink']   = unicode( config['root']+alist[0]['href']  );
        
        title = unicode( alist[1].contents[0] );  
        item['title']       = unicode( title            );
        
        item['titlelink']   = unicode( config['root']+alist[1]['href']  );
        if config['hasauthor'] :
            if config['authortag'] == 'a' :
                item['author']       = unicode( alist[2].contents[0]        );
                item['authorlink']   = unicode( config['root']+alist[2]['href'] );
            else :
                item['author']       = unicode( dom_row.findAll( config['authortag'] )[config['authorindex']].contents[0] );
                
        if config['haspostcount']:
            item['postcount']   = unicode( dom_row('td')[ config['postcountindex'] ].contents[0] );   
        else:
            item['postcount'] = '0';
        parsed_result.append( item );    
    
    return{
           'itemlist':parsed_result,
           'name':config['name'],
           'chinesename':config['chinesename'],
                    }
        
    
    
    
    
def parsebbs_byXpath( bbsconfig  ):
    htmlstring  = urllib2.urlopen( bbsconfig['locate'] ).read();
    htmlstring  = unicode(htmlstring,'GBK','ignore').encode('UTF-8') ;
    dom         = BeautifulSoup(htmlstring);
    contentpath = Path( bbsconfig['xpath'] );
    domblock    = contentpath.apply(dom);
    domblock    = BeautifulSoup ( convertdom2string( domblock ) );
    
    return parse_subdom_item( domblock,bbsconfig); 

def parsebbsbyId( bbsconfig , tag, oid  ):
    htmlstring  = urllib2.urlopen( bbsconfig['locate'] ).read();
    htmlstring  = unicode(htmlstring,'GBK','ignore').encode('UTF-8') ;
    dom         = BeautifulSoup(htmlstring);
    domblock = dom.find( tag, id = oid );
    #list_str = unicode( resultdom );
    
    return parse_subdom_item( domblock,bbsconfig);

def parsebbsbytableborder( bbsconfig, borderlen ):
    htmlstring  = urllib2.urlopen( bbsconfig['locate'] ).read();
    htmlstring  = unicode(htmlstring,'GBK','ignore').encode('UTF-8') ;
    dom         = BeautifulSoup(htmlstring);
    domblock = dom.find( 'table', border = borderlen );
    
    
    return parse_subdom_item( domblock,bbsconfig);


    
    
    
def freshbbs( ):
    
    sjtubbs = {
        'locate':'http://bbs.sjtu.edu.cn/php/bbsindex.html',
        'root':'http://bbs.sjtu.edu.cn/',
        'xpath':'/html/body/form/table[3]/tr/td/table[2]/tr/td[2]/table/tr[2]/td/table',
        'skiphead':False,
        'skiptail':True,
        'lineindicator':'tr',
        'hasauthor':True,
        'haspostcount':False,
        'authortag':'td',
        'authorindex':2,
        'name':'sjtu',
        'chinesename':u'饮水思源',
    };
    
    smthbbs = {
        'locate':'http://bbs.tsinghua.edu.cn/mainpage.php',
        'root':'http://bbs.tsinghua.edu.cn',
        'xpath':'/html/body/table[3]/tr/td/table[2]/tr[3]/td',
        'skiphead':False,
        'skiptail':False,
        'lineindicator':'li',
        'hasauthor':True,
        'haspostcount':False,
        'authortag':'a',
        'authorindex':2,
        'name':'smth',
        'chinesename':u'水木清华',
    };  
    
    lilibbs = {
        'locate':'http://bbs.nju.edu.cn/bbstop10',
        'root':'http://bbs.nju.edu.cn/',
        'xpath':'/html/center/table',
        'skiphead':True,
        'skiptail':False,
        'lineindicator':'tr',
        'hasauthor':True,
        'haspostcount':True,
        'postcountindex':4,
        'authortag':'a',
        'authorindex':2,
        'name':'lily',
        'chinesename':u'小百合',
    };
    
    fudanbbs = {
        'locate':'http://bbs.fudan.edu.cn/cgi-bin/bbs/bbstop10',
        'root':'http://bbs.fudan.edu.cn/cgi-bin/bbs/',
        'xpath':'/html/center/table/tr[2]/td[2]/table',
        'skiphead':True,
        'skiptail':False,
        'lineindicator':'tr',
        'hasauthor':True,
        'haspostcount':True,
        'postcountindex':4,
        'authortag':'a',
        'authorindex':2,
        'name':'fudan',
        'chinesename':u'日月光华',
    };
    
    
    xjtubbs = {
        'locate':'http://bbs.xjtu.edu.cn/BMYELAVBXDPIOAJBDICRKENIKWXEIKSVQZJU_B/bbstop10',
        'root':'http://bbs.xjtu.edu.cn/BMYELAVBXDPIOAJBDICRKENIKWXEIKSVQZJU_B/',
        'xpath':'/body/center/table',
        'skiphead':True,
        'skiptail':False,
        'lineindicator':'tr',
        'hasauthor':False,
        'haspostcount':True,
        'postcounttag':'td',
        'postcountindex':3,
        'name':'xjtu',
        'chinesename':u'兵马俑',

    };
    
    
    ustcbbs = {
        'locate':'http://bbs.ustc.edu.cn/cgi/bbstop10',
        'root':'http://bbs.ustc.edu.cn/cgi/',
        'xpath':'/html/center/table',
        'skiphead':True,
        'skiptail':False,
        'lineindicator':'tr',
        'hasauthor':True,
        'authortag':'td',
        'authorindex':3,
        'haspostcount':False,
        'haspostcount':True,
        'postcountindex':4,
        'name':'ustc',
        'chinesename':u'瀚海星云',
        
    };
    
    
    
    
    
    context = [
        parsebbs_byXpath(sjtubbs),
        parsebbsbyId( smthbbs,'ul','toptenlist'),
        parsebbs_byXpath(lilibbs),
        parsebbs_byXpath( fudanbbs ),
        parsebbsbytableborder(xjtubbs,'1'),
        parsebbsbytableborder(ustcbbs,'0')
    ]
    
    for bbsinfoitem in context:
        PutBbsInfo(bbsinfoitem);
    
    return;
    
def getFreshBBS( request ):
    freshbbs();
    return getbbs( request);

def getbbs( request ):
    bbslist = [];
    for school in  HighSchoolBbs.all():
        toptenlist = TopTenItem.gql('where school = :1 ORDER BY order ASC',school);

        bbsinfo = {
                    'name': unicode(school.schoolname),
                    'chinesename':unicode(school.chinesename),
                    'itemlist':toptenlist,
                    }
        bbslist.append( bbsinfo);
    
    return render_to_response('BBS_PARSE.html', {'context':bbslist});
                    

def PutBbsInfo( bbsinfo ):
    
   
    qSchool = HighSchoolBbs.gql("WHERE schoolname = :1", bbsinfo['name'] );
    if( qSchool.count() > 0 ):
        nschool = qSchool[0];
    else:
        nschool = HighSchoolBbs( schoolname= unicode(bbsinfo['name']), chinesename = unicode(bbsinfo['chinesename']));
        nschool.put();
    code = sys.getdefaultencoding()

    qTopTenItem = TopTenItem.gql('where school = :1',nschool);
    
    for item in qTopTenItem :
        item.delete();
    itemlist = bbsinfo['itemlist'];
    
    for i in range( len(itemlist) ):
        item = itemlist[i];
        Titem = TopTenItem( board       = item['board'],
                            boardlink   = item['boardlink'],
                            title       = db.Text(item['title']),
                            titlelink   = item['titlelink'],
                            author      = item['author'],
                            authorlink  = item['authorlink'],
                            postcount   = int(item['postcount']),
                            order       = i,
                            school      = nschool);

        Titem.put();
    
    return;
                            
    




