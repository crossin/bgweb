# coding=utf-8
import re;
sjtubbs = {
        'locate':'http://bbs.sjtu.edu.cn/php/bbsindex.html',
        'root':'http://bbs.sjtu.edu.cn/',
        'xpath':'/html/body/form/table[3]/tr/td/table[2]/tr/td[2]/table/tr[2]/td/table',
        'dom_row_pattern' :"""
            <tr>
            <td >[<a href="$boardlink">$board</a>]</td>
            <td><a href="$titlelink">$title</a></td>
            <td>$author</td>
            </tr>
        """,
        'name':'sjtu',
        'chinesename':u'饮水思源',
        'rank':1,
    };
    
smthbbs = {
        'locate':'http://bbs.tsinghua.edu.cn/mainpage.php',
        'root':'http://bbs.tsinghua.edu.cn',
        'xpath':'/html/body/table[3]/tr/td/table[2]/tr[3]/td',
        'name':'smth',
        'chinesename':u'水木清华',
        'dom_row_pattern' : """
            <li>
            <a href="$boardlink">$board</a>*
            <a href="$titlelink">$title</a>*
            <a href="$authorlink">$author</a>
            </li>
        """,
        're_block':re.compile(r'<ul id="toptenlist">.*?</ul>',re.DOTALL),
        'rank':2,
    };
     
newsmth = {
        'locate':'http://www.newsmth.net/rssi.php?h=1',
        'root':'',
        'name':'smth2',
        'chinesename':u'水木社区',
        'dom_row_pattern' : """
            <item>
            <title>$title</title>
            <link>$titlelink</link>
            <author>$author</author>
            <pubDate>*</pubDate>
            <guid>$boardlink</guid>
            <description>*</description>
            </item>
        """,
        're_block':re.compile(r'<rss version="2.0">.*?</rss>',re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)',re.DOTALL),
        'encoding':'utf8',
        'rank':2,
    }; 

tjbbs = {
        'locate':'http://bbs.tongji.edu.cn/rssi.php?h=1',
        'root':'',
        'name':'tongji',
        'chinesename':u'同舟共济',
        'dom_row_pattern' : """
            <item>
            <title>$title</title>
            <link>$titlelink</link>
            <author>$author</author>
            <pubDate>*</pubDate>
            <guid>$boardlink</guid>
            <description>*</description>
            </item>
        """,
        're_block':re.compile(r'<rss version="2.0">.*?</rss>',re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)',re.DOTALL),
        'encoding':'utf8',
        'rank':5,
    }; 
    
lilybbs = {
        'locate':'http://bbs.nju.edu.cn/bbstop10',
        'root':'http://bbs.nju.edu.cn/',
        'xpath':'/html/center/table',
        'name':'lily',
        'chinesename':u'小百合',
        'dom_row_pattern' : """
            <tr>
            <td>*
            <td><a href="$boardlink">$board</a>
            <td><a href="$titlelink">$title</a>
            <td><a href="$authorlink">$author</a>
            <td>$postcount
        """,
        're_block':re.compile(r'<table width=640>.*?</table>',re.DOTALL),
        'rank':3,
    };
    
zjubbs = {
        'locate':'http://www.freecity.cn/agent/top10.do',
        'root':'http://www.freecity.cn/agent/',
        'name':'zju',
        'chinesename':u'飘渺水云间',
        'dom_row_pattern' : """
            <tr>
            <td>*</td>
            <td><a href="$boardlink">$board</a></div>
            <td>
                <a href="$titlelink">$title</a>
                *
            </td>
            <td><a onclick="$authorlink">$author</a></td>
            <td>*</td>
            <td>$postcount</td>
            <td>*</td>
            </tr>
        """,
        're_block':re.compile(r'<table .*?>.*?</table>',re.DOTALL),
        'rank':4,
        
    };
    
fudanbbs = {
        'locate':'http://bbs.fudan.edu.cn/cgi-bin/bbs/bbstop10',
        'root':'http://bbs.fudan.edu.cn/cgi-bin/bbs/',
        'xpath':'/html/center/table/tr[2]/td[2]/table',
        'name':'fudan',
        'chinesename':u'日月光华',
        'dom_row_pattern' : """
            <tr>
            <td>*</td>
            <td><a href="$boardlink"><b>$board</b></a></td>
            <td><a href="$titlelink">$title</a></td>
            <td><a href="$authorlink"><b>$author</b></a></td>
            <td>$postcount</td>
            </tr>
        """,
        're_block':re.compile(r'<table border=0 width=100%>.*?</table>',re.DOTALL),
        'rank':5,
    };
    
nankaibbs = {
        'locate':'http://bbs.nankai.edu.cn/hottopic10.htm',
        'root':'http://bbs.nankai.edu.cn/',
        'xpath':'/html/center/table/tr[2]/td[2]/table',
        'name':'nankai',
        'chinesename':u'我爱南开',
        'dom_row_pattern' : """
             <tr>
             <td>
             <a href="$titlelink">$title</a>
             <a href="$authorlink">$author</a>
             </td>
             <td>
             <a href="$boardlink">$board</a>
             </td>
             <td>*</td>
             </tr>
        """,
        're_block':re.compile(r'<table .*?>.*?</table>',re.DOTALL|re.I),
        'rank':6,
    };
    
    
xjtubbs = {
        'locate':'http://bbs.xjtu.edu.cn/BMYELAVBXDPIOAJBDICRKENIKWXEIKSVQZJU_B/bbstop10',
        'root':'http://bbs.xjtu.edu.cn/BMYELAVBXDPIOAJBDICRKENIKWXEIKSVQZJU_B/',
        'xpath':'/body/center/table',
        'name':'xjtu',
        'chinesename':u'兵马俑',
        'dom_row_pattern' : """
            <tr>
            <td>*</td>
            <td><a href="$boardlink">$board</a></td>
            <td><a href="$titlelink">$title</a></td>
            <td>$postcount</td>
            </tr>
        """,
        're_block':re.compile(r'<table border=1>.*?</table>',re.DOTALL),
        'rank':6,

    };
whubbs = {
        'locate':'http://bbs.whu.edu.cn/mainpage.html',
        'root':'http://bbs.whu.edu.cn/',
        'xpath':'/html/body/div[2]/table/tr/td/fieldset',
        'name':'whu',
        'chinesename':u'珞珈山水',
        'dom_row_pattern' : """
            <li>
            <img>
            <a href="$titlelink">$title</a>
            *
            <a href="$boardlink">$board</a>
            *
            </li>
        """,
        #'re_block':re.compile(r'<legend>今日推荐精彩话题</legend><ul>.*?</ul>',re.DOTALL),
        'rank':6,

    };
    
xmubbs = {
        'locate':'http://bbs.xmu.edu.cn/xmuxml/hot10.xml',
        'root':'',
        'name':'xmu',
        'chinesename':u'鼓浪听涛',
        'dom_row_pattern' : """
            <item>
            <title>$title</title>
            <link>$titlelink</link>
            <author>$author</author>
            <pubDate>*</pubDate>
            <guid>$boardlink</guid>
            <description>*</description>
            </item>
        """,
        're_block':re.compile(r'<rss version="2.0">.*?</rss>',re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)',re.DOTALL),
        'encoding':'utf8',
        'rank':5,
    }; 
    
    
ustcbbs = {
        'locate':'http://bbs.ustc.edu.cn/cgi/bbstop10',
        'root':'http://bbs.ustc.edu.cn/cgi/',
        'xpath':'/html/center/table',
        'name':'ustc',
        'chinesename':u'瀚海星云',
        'dom_row_pattern' : """
            <tr>
            <td>*
            <td><a href="$boardlink">$board</a>
            <td><a href="$titlelink">$title</a>
            <td><a href="$authorlink">$author</a>
            <td>$postcount
        """,
        're_block':re.compile(r'<table border=0 width=90%>.*?</table>',re.DOTALL),
        'rank':7,
        
    };
    
zsubbs = {
        'locate':'http://bbs.zsu.edu.cn/',
        'root':'http://bbs.zsu.edu.cn',
        'name':'zsu',
        'chinesename':u'逸仙时空',
        'dom_row_pattern' : """
            <li>
            <span><a href="$titlelink">$title</a> 
            [<a href="$boardlink" >$board</a>]</span>
            </li>
        """,
        're_block':re.compile(r'<div id="topten">.*?</div>',re.DOTALL),
        'rank':7,
        
    };
    
dlutbbs = {
        'locate':'http://bbs.dlut.edu.cn/rssi.php?h=1',
        'root':'',
        'name':'dlut',
        'chinesename':u'碧海青天站',
        'dom_row_pattern' : """
            <item>
            <title>$title</title>
            <link>$titlelink</link>
            <author>$author</author>
            <pubDate>*</pubDate>
            <guid>$boardlink</guid>
            <description>*</description>
            </item>
        """,
        're_block':re.compile(r'<rss version="2.0">.*?</rss>',re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)',re.DOTALL),
        'encoding':'utf8',
        'rank':10,
    }; 

njuptbbs = {
        'locate':'http://bbs.njupt.edu.cn/cgi-bin/bbstop10',
        'root':'http://bbs.njupt.edu.cn/cgi-bin/',
        'name':'njupt',
        'chinesename':u'紫金飞鸿',
        'dom_row_pattern' : """
            <tr>
            <td>*
            <td><a href="$boardlink">$board</a>
            <td><a href="$titlelink">$title</a>
            <td><a href="$authorlink">$author</a>
            <td>$postcount
        """,
        're_block':re.compile(r'<table border=1 width=610>.*?</table>',re.DOTALL),
        'rank':10,
        
    };
    
csubbs = {
        'locate':'http://bbs.csu.edu.cn/top10_rss.xml',
        'root':'',
        'name':'CSU',
        'chinesename':u'云麓园',
        'dom_row_pattern' : """
            <item>
                <dc:format>*</dc:format>
                <dc:source>*</dc:source>
                <dc:creator>$author</dc:creator>
                <title>$title</title>
                <link>$titlelink</link>
                *
            </item>
        """,
        're_block':re.compile(r'<rdf:RDF.*?>.*?</rdf:RDF>',re.DOTALL),
        'rank':7,
    }; 

jlubbs = {
        'locate':'http://bbs.jlu.edu.cn/cgi-bin/bbssec',
        'root':'http://bbs.jlu.edu.cn/cgi-bin/',
        'xpath':'/html/body/table/tr/td/table/tr[4]/td/table/tr/td[2]/table',
        'name':'jlu',
        'chinesename':u'牡丹园',
        'dom_row_pattern' : """
            <tr>
            <td>◆<a href="$titlelink">$title</a>
            </td>
            </tr>   
        """,
        #'re_block':re.compile(r'<legend>今日推荐精彩话题</legend><ul>.*?</ul>',re.DOTALL),
        'rank':10,

    };
    
    

    
