# coding=utf-8

__author__ = "zinking3@gmail.com"
__version__ = "0.1"
__license__ = "GPL"

import sys
default_encoding = 'utf-8'
if sys.getdefaultencoding() != default_encoding:
    reload(sys)
    sys.setdefaultencoding(default_encoding)


from google.appengine.api import *
from ragendja.dbutils import *;
from datetime import *;

from BeautifulSoup import BeautifulSoup;
from bsoupxpath import Path;
from customized_soup import CustomizedSoup;
from scraper import Scraper;

import htmlentitydefs;

import re,copy,string,logging,time;
import urllib,urllib2,Cookie;

from pageharvest.settings import *;
from content.models       import *;

def report_parse_exceptions( content ):
    logging.info("Reporting parse problems to administrators" );
    mail.send_mail(sender="BBS TOP 10<bbstop10@appspot.com>",
              to="Albert <zinking3@gmail.com>",
              subject="Parsing Problem Report - BBSTOP10",
              body=content)

def unescape(text):
   """Removes HTML or XML character references 
      and entities from a text string.
      keep &amp;, &gt;, &lt; in the source code.
   from Fredrik Lundh
   http://effbot.org/zone/re-sub.htm#unescape-html
   """
   def fixup(m):
      text = m.group(0)
      if text[:2] == "&#":
         # character reference
         try:
            if text[:3] == "&#x":
               return unichr(int(text[3:-1], 16))
            else:
               return unichr(int(text[2:-1]))
         except ValueError:
            #print "erreur de valeur"
            pass
      else:
         # named entity
         try:
            if text[1:-1] == "amp":
               text = "&amp;amp;"
            elif text[1:-1] == "gt":
               text = "&amp;gt;"
            elif text[1:-1] == "lt":
               text = "&amp;lt;"
            else:
               #print text[1:-1]
               text = unichr(htmlentitydefs.name2codepoint[text[1:-1]])
         except KeyError:
            #print "keyerror"
            pass
      return text # leave as is
   return re.sub("&#?\w+;", fixup, text)
def make_cookie_header(cookie):
    ret = ""
    for val in cookie.values():
        ret+="%s=%s; "%(val.key, val.value)
    return ret
from util import twitter;
from util import bitly;
class Microblog(object):
    def __init__(self): 
        self.name = SINA_163_USERNAME;
        self.password = SINA_163_PASSWORD;
        self.skip_n163 = False;
        self.skip_sina = False;
        self.skip_twitter = False;
        
        self.login_to_sina_microblog();
        self.login_to_net163_microblog();

        self.twitter_api = twitter.Api(username=TWITTER_API_USERNAME, password=TWITTER_API_PASSWORD);
        self.bitly_api   =  bitly.Api(login=BITLY_API_USERNAME, apikey=BITLY_API_APIKEY); 

        result = 5;
        if( self.skip_n163 ): result -= 2;
        if( self.skip_sina ): result -= 2;
        if( self.skip_twitter ): result -=2;
        self.quota = result;

    

    def login_to_sina_microblog(self):
        try:
            self.sinahttp = urlfetch.fetch(
                url="https://login.sina.com.cn/sso/login.php?username=%s&password=%s&returntype=TEXT"%(self.name,self.password));
        except Exception,e:
            self.skip_sina = True;
            logging.error( "ERROR OCCURED WHEN logging to sina mblog " + str(e) );
        self.sinacookie = Cookie.SimpleCookie(self.sinahttp.headers.get('set-cookie', ''));#TBD
    def login_to_net163_microblog(self):
        try:
            self.n163http = urlfetch.fetch(
                url="https://reg.163.com/logins.jsp?username=%s&password=%s&product=t&type=1"%(self.name,self.password));
        except Exception,e:
            self.skip_n163 = True;
            logging.error( "ERROR OCCURED WHEN logging to 163 mblog " + str(e) );
        self.n163cookie = Cookie.SimpleCookie(self.n163http.headers.get('set-cookie', ''));
        
    def post_n163_msg(self,msg):
        if( self.skip_n163 ): return;
        msg=unescape(msg)
        form_fields = {
          "status": msg,          
        }
        form_data = urllib.urlencode(form_fields);
        try:
            result = urlfetch.fetch(url="http://t.163.com/statuses/update.do",
                                payload=form_data,
                                method=urlfetch.POST,
                                headers={'Referer':'http://t.163.com','Cookie' : make_cookie_header(self.n163cookie)})
        except Exception,e:
            logging.error( "ERROR OCCURED WHEN SENDING MBLOG TO 163 " + str(e) );

        
    def post_sina_msg(self, msg ):
        if( self.skip_sina ): return;       
        msg=unescape(msg);
        form_fields = {
          "content": msg,          
        }
        form_data = urllib.urlencode(form_fields)
        
        try:
            result = urlfetch.fetch(url="http://t.sina.com.cn/mblog/publish.php",
                                payload=form_data,
                                method=urlfetch.POST,
                                headers={'Referer':'http://t.sina.com.cn','Cookie' : make_cookie_header(self.sinacookie)})
        except Exception,e:
            logging.error( "ERROR OCCURED WHEN SENDING MBLOG TO SINA " + str(e) );
        

    
    def post_twitter_msg(self, item ):
        short_url = item['link'];
        try:
            short_url = self.bitly_api.shorten( item['link'] );
        except Exception,e:
            logging.error( "ERROR OCCURED WHEN SHORTENING URL WITH BITLY " + str(e) );
            return;
        msg=item['pattern'] %( item['schoolname'], item['title'], short_url, item['author'] );
        msg=unescape(msg);
        try:
            self.twitter_api.PostUpdate( msg );
        except Exception,e:
            logging.error( "ERROR OCCURED WHEN POSTING MBLOG TO TWITTER " + str(e) );

class BBSParser(object):
    def __init__(self): 
        pass;
    
    def convertdom2string(self, domlist):
        list_str = u'';
        for i in range(len(domlist)):
            list_str += unicode(domlist[i]);
        return list_str;

    def save_parsed_links(self, linklist , config):
        schoolbbs = get_object(Schoolbbs, 'schoolname =', config['schoolname']);
        if schoolbbs:
            for link in linklist:
                linkobject = get_object(Bbslinks, 'titlelink =', link['titlelink']);
                if  linkobject:
                    linkobject.updatetime = datetime.now();
                    linkobject.put();
                else:
                    resultlink = {};
                    for pair in link.items():
                        resultlink[ str( pair[0] ) ] =  unicode( pair[1] ) ;
                    resultlink['school'] = schoolbbs;
                    now = datetime.now();
                    schoolbbs.lastfresh = now;
                    link = db_create(Bbslinks,  createtime=now, updatetime=now,
                        **resultlink
                    );
                    schoolbbs.put();                   
            config['lastfresh'] = schoolbbs.lastfresh;
        else:
            raise;

    def parsebbs(self, config, configitem ):
        t1 = time.time();
        try: 
            htmlstring = urllib2.urlopen(config['locate']).read();
            configitem.totalparse = configitem.totalparse + 1;
            configitem.rank = configitem.rank - 1;
        except Exception, e: 
            configitem.failedparse = configitem.failedparse + 1;
            error_msg = "Failed to open following url %s of school: %s" % (config['locate'], config['bbsname']);
            logging.error( error_msg );
            configitem.put();
            return 0;
            
        if (config['encoding'] == 'utf8' ):
            htmlstring = htmlstring;
        else:
            htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');

        try:

            if( config['needXpath'] ):
                    linklist = self.parsebbsbyXpath(config , htmlstring);           
            else:
                    linklist = self.parsebbsbyRegularExpression(config , htmlstring);
        except Exception, e:
            logging.error("failed to parse required content SITE structure changed; schoolname= %s"%( config['bbsname'] ) );
            logging.error("Detailed Exception:%s"%(e));
            configitem.put();
            return 0;
        
            
        t2 = time.time();
            
        self.save_parsed_links(linklist, config);
        delta = (t2-t1)*1000;
        configitem.totalparsetime = configitem.totalparsetime + delta;
        logging.debug("Successfully parsing school:%s costing %d milliseconds;" % (config['bbsname'], delta ));
        configitem.lastfresh = datetime.now();
        configitem.status = STATUS_NORMAL;
        configitem.put();
        return delta;


    def parsebbsbyXpath(self, config, htmlstring):
        try:
            dom = BeautifulSoup(htmlstring);
        except Exception, e:
            logging.error("failed to parse bbs by Xpath parser; schoolname= %s", config['bbsname']);
            raise;
        contentpath = Path(config['xpath']);
        domblock = contentpath.apply(dom);
        blockstring = self.convertdom2string(domblock) ;

        if blockstring is  None :
            logging.error("failed to parse bbs by xpath parser; schoolname= %s", config['bbsname']);
            return;
        return self.parsebbsDomDetail(blockstring, config);
    
    def parsebbsbyRegularExpression(self, config, htmlstring):
        try:
            re_block = config['re_block'];
            blockstring = re_block.search(htmlstring).group();
        except Exception, e: 
            logging.error("failed to parse bbs by RE parser; schoolname= %s", config['bbsname']);
            raise;
        return self.parsebbsDomDetail(blockstring, config);
    
    #TBD finish this in a more reasonable way
    def fixitem(self, item , config):
        orginal_link = item['titlelink'];
        item['titlelink'] = config['root'] + item['titlelink'];
        if ( 'additional' in config.keys() and config['additional'] == 'special' ):
            item['titlelink'] = config['root'] %( item['board'],orginal_link);
        if ('re_board' in config.keys()):
            re_board = config[ 're_board' ];
            titlegroup = re_board.search(item['title']);
            item['board' ] = titlegroup.group('board');
            item['title' ] = titlegroup.group('title');
            
        if ('re_board1' in config.keys()):
            re_board = config[ 're_board1' ];
            titlegroup = re_board.search(item['titlelink']);
            item['board' ] = titlegroup.group('board');
            
    #return links list
    def parsebbsDomDetail(self, dom_block_str , config):     
        try:
            dom_row_pattern = config['dom_row_pattern']; 
            #make dom block string become dom again, 
            #Unreasonable for: string->dom->blockdom->blockstring->blockdom->rowdom->rowstring need to be revised
            doc = CustomizedSoup(dom_block_str);        
            scraper = Scraper(dom_row_pattern);         #setup scraper to scrape row string
            ret = scraper.match(doc);
            parsed_result = []; index = 1;
            msg = "totally %d items parsed for school %s " %( len(ret), config['locate'] );
            logging.info(msg);
            for item in ret:
                value = scraper.extract(item); 
                self.fixitem(value, config);
                value['title'] = unescape( value['title'] );#SAFE TITLE
                parsed_result.append(value);
                index = index + 1;
                if index > 10:break;
        except Exception, e: 
            logging.error("failed to parse bbs in Domdetail ;schoolname= %s", config['locate']);
            logging.error("Caught Exception:%s",e);
            raise;         
        return  parsed_result;
        
        
