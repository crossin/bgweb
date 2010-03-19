# coding=utf-8

__author__ = "zinking3@gmail.com"
__version__ = "0.1"
__license__ = "GPL"
from google.appengine.api import urlfetch
from BeautifulSoup      import BeautifulSoup;
from bsoupxpath         import Path;
from customized_soup    import CustomizedSoup;
from scraper            import Scraper;
#from model.models       import *
from bbs_parse_settings import *;
from settings           import *;
from ragendja.dbutils       import *;
from content.models         import *;
from datetime import *;

from google.appengine.api import mail;

import urllib2;
import re;
import copy;
import string;
import logging;
import time;

def report_parse_exceptions( content ):
    logging.info("Reporting parse problems to administrators" );
    mail.send_mail(sender="BBS TOP 10<bbstop10@appspot.com>",
              to="Albert <zinking3@gmail.com>",
              subject="Parsing Problem Report - BBSTOP10",
              body=content)


class BBSParser(object):
    def __init__(self):       
        pass;
    
    
    def convertdom2string(self, domlist):
        list_str = u'';
        for i in range(len(domlist)):
            list_str += unicode(domlist[i]);
        return list_str;

  
    """
    def getDomString(self, config):
        try: 
            htmlstring = urllib2.urlopen(config['locate']).read();
        except Exception, e: 
            logging.error("Failed to open following url %s of school: %s" %( config['locate'],config['bbsname'] ) );
            raise;
            
        #convert encodings to recoginizable charsets 
        htmlstring = u'';
        try:
            if ('encoding' in config.keys()):
                if config['encoding'] == 'utf8':
                    return htmlstring;
            htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');
        except Exception, e: 
            print type( e );
            print "conversion error";
        return htmlstring;
    """
        
    def save_parsed_links(self, linklist , config):
        #now         = datetime.now();
        schoolbbs = get_object(Schoolbbs, 'schoolname =', config['schoolname']);
        if schoolbbs:
            for link in linklist:
                
                linkobject = get_object(Bbslinks, 'titlelink =', link['titlelink']);
                if  linkobject:
                    linkobject.updatetime = datetime.now();
                    #print "update link %s at time %s"%(link['titlelink'], datetime.now() ) 
                else:
                    #print link;
                    resultlink = {};#converting the fucking unicode map into str
                    for pair in link.items():
                        resultlink[ str( pair[0] ) ] =  unicode( pair[1] ) ;
                    resultlink['school'] = schoolbbs;
                    #print 'this is link ->' + link;
                    now = datetime.now();
                    schoolbbs.lastfresh = now;
                    db_create(Bbslinks,  createtime=now, updatetime=now,
                        #board=unicode(link['board']), title=unicode(link['title']) , author=unicode(link['author']), titlelink=unicode(link['titlelink'])
                        **resultlink
                    );
                    #print 'this is result link ->' + resultlink;
                    schoolbbs.put();
                    #print "put new link%s into database"%(link['titlelink']);
            #schoolbbs['lastfresh'] = datetime.now();
            config['lastfresh'] = schoolbbs.lastfresh;
        else:
            raise;
        
        
        

    def parsebbs(self, config, configitem ):
        t1 = time.time();
        try: 
            htmlstring = urllib2.urlopen(config['locate'], timeout=3).read();
            configitem.totalparse = configitem.totalparse + 1;
            configitem.rank = configitem.rank - 1;
        except Exception, e: 
            configitem.failedparse = configitem.failedparse + 1;
            #configitem.rank = configitem.rank + 2;
            #configitem.status = STATUS_UNREACHABLE;
            error_msg = "Failed to open following url %s of school: %s" % (config['locate'], config['bbsname']);
            logging.error( error_msg );
            #report_parse_exceptions( error_msg );
            configitem.put();
            return 0;
            
        if (config['encoding'] == 'utf8' ):
            #if config['encoding'] != 'utf8':
            htmlstring = htmlstring;
            #return htmlstring; there are conversion exceptions
        else:
            htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');

        try:

            if( config['needXpath'] ):
                    linklist = self.parsebbsbyXpath(config , htmlstring);           
            else:
                    linklist = self.parsebbsbyRegularExpression(config , htmlstring);
        
        except Exception, e:
            print type(e);
            logging.error("failed to parse required content SITE structure changed; schoolname= %s", config['bbsname']);
            configitem.status = STATUS_EXCEPTION;
            configitem.put();
            return 0;
        
            
        t2 = time.time();
            
        self.save_parsed_links(linklist, config);
        delta = (t2-t1)*1000;
        configitem.totalparsetime = configitem.totalparsetime + delta;
        logging.debug("Successfully parsing school:%s costing %d milliseconds;" % (config['bbsname'], delta ));
        #logging.debug("Parsing school:%s Average cost %d milliseconds;" % (config['bbsname'], configitem.getAverageParseTime() ));
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
            #return;
            

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
            #return;
        return self.parsebbsDomDetail(blockstring, config);
    
    #TBD finish this in a more reasonable way
    def fixitem(self, item , config):
        """
        if ('postcount' in item.keys() ):
            item['postcount'] = int( item['postcount'] );
        else:
            item['postcount'] = 0;
        """
        #item['postcount'] = 0;
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
            #values = scraper.extract(ret[0]);
            parsed_result = []; 
            index = 1;

            for item in ret:
                value = scraper.extract(item); 
                self.fixitem(value, config);
                #value['boardlink']  = config['root'] + value['boardlink'];
                #value['titlelink'] = config['root'] + value['titlelink'];
                #print value['titlelink']
                
                #value['authorlink'] = config['root'] + value['authorlink'];

                parsed_result.append(value);
                index = index + 1;
                if index > 10:break;
        except Exception, e: 
            logging.error("failed to parse bbs in Domdetail ;schoolname= %s", config['locate']);
            print e;
            raise;
                    
        return  parsed_result;
        

        
