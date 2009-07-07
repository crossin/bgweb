# coding=utf-8

__author__ = "zinking3@gmail.com"
__version__ = "0.1"
__license__ = "GPL"
from google.appengine.api import urlfetch
from BeautifulSoup      import BeautifulSoup;
from bsoupxpath         import Path;
from customized_soup    import CustomizedSoup;
from scraper            import Scraper;


import urllib2;
import re;
import copy;
import string;
import logging;

class BBSParser(object):
    def __init__(self):       
        pass;
    
    
    def convertdom2string(self, domlist):
        list_str = u'';
        for i in range(len(domlist)):
            list_str += unicode(domlist[i]);
        return list_str;

    def parse_subdom_item(subdom, config):
        parsed_result = [];
        trlist = subdom.findAll(config['lineindicator']); 
        if (config['skiphead']): 
            start_index = 1;
        else:
            start_index = 0;
    
        
        itr_len = len(trlist) - start_index;
        if config['skiptail'] :
            itr_len = itr_len - 1;
            
        if itr_len > 10:
           itr_len = 10;
            
        for i in range(itr_len):
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
            item['board'] = unicode(alist[0].contents[0]);
            item['boardlink'] = unicode(config['root'] + alist[0]['href']);
            
            title = unicode(alist[1].contents[0]);  
            item['title'] = unicode(title);
            
            item['titlelink'] = unicode(config['root'] + alist[1]['href']);
            if config['hasauthor'] :
                if config['authortag'] == 'a' :
                    item['author'] = unicode(alist[2].contents[0]);
                    item['authorlink'] = unicode(config['root'] + alist[2]['href']);
                else :
                    item['author'] = unicode(dom_row.findAll(config['authortag'])[config['authorindex']].contents[0]);
                    
            if config['haspostcount']:
                item['postcount'] = unicode(dom_row('td')[ config['postcountindex'] ].contents[0]);   
            else:
                item['postcount'] = '0';
            parsed_result.append(item);    
        
        return{
               'itemlist':parsed_result,
               'name':config['name'],
               'chinesename':config['chinesename'],
                        }
                   
        
    

    def getDomString(self, config):
        try: 
            htmlstring = urllib2.urlopen(config['locate']).read();
        except Exception, e: 
            logging.debug("failed to open following url %s", config['locate']);
            return 'error';
        if ('encoding' in config.keys()):
            if config['encoding'] == 'utf8':
                return htmlstring;
        htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');
        return htmlstring;
    


    def parsebbsbyXpath(self, config):
        htmlstring = self.getDomString(config);
        if htmlstring == 'error':
            return;
        dom = BeautifulSoup(htmlstring);
#        logging.info(dom);
        contentpath = Path(config['xpath']);
        domblock = contentpath.apply(dom);
        blockstring = self.convertdom2string(domblock) ;
#        logging.info(blockstring);
        if blockstring is  None :
            return;
        return self.parsebbsDomDetail(blockstring, config);
    
    def parsebbsbyRegularExpression(self, config):
        htmlstring = self.getDomString(config);
        if htmlstring == 'error':
            return;
#        logging.info(htmlstring);
        re_block = config['re_block'];
        blockstring = re_block.search(htmlstring).group();
#        logging.info(blockstring);
        if blockstring is  None :
            return;#error occured
        return self.parsebbsDomDetail(blockstring, config);
    
    def fixitem(self, item , config):
        if ('author' not in item.keys()):
            item['author' ] = '';
        if ('authorlink' not in item.keys()):
            item['authorlink' ] = '';
        if ('board'  not in item.keys()):
            item['board'] = '';
        if ('boardlink'  not in item.keys()):
            item['boardlink'] = '';
        if ('postcount' not in item.keys()):
            item['postcount' ] = 0;
        if ('re_board' in config.keys()):
            re_board = config[ 're_board' ];
            titlegroup = re_board.search(item['title']);
            item['board' ] = titlegroup.group('board');
            item['title' ] = titlegroup.group('title');
        if ('re_board1' in config.keys()):
            re_board = config[ 're_board1' ];
            titlegroup = re_board.search(item['titlelink']);
            item['board' ] = titlegroup.group('board');
            
    
    def parsebbsDomDetail(self, dom_block_str , config):     
        dom_row_pattern = config['dom_row_pattern'];
        doc = CustomizedSoup(dom_block_str);
        scraper = Scraper(dom_row_pattern);
        ret = scraper.match(doc);
        #values = scraper.extract(ret[0]);
        parsed_result = []; 
        index = 1;
        for item in ret:
            value = scraper.extract(item); 
            self.fixitem(value, config);
            value['boardlink'] = config['root'] + value['boardlink'];
            value['titlelink'] = config['root'] + value['titlelink'];
            value['authorlink'] = config['root'] + value['authorlink'];
            self
            parsed_result.append(value);
            index = index + 1;
            if index >= 11:
                break;
        
                    
        return{
               'itemlist':parsed_result,
               'config':config, };
        

        
