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
        'bbsname':'sjtu',
        'schoolname':u'上海交通大学',
        'chinesename':u'饮水思源',
        'rank':1,
        'needXpath':True,
    };

     
newsmth = {
        'locate':'http://www.newsmth.net/rssi.php?h=1',
        'root':'',
        'bbsname':'smth2',
        'schoolname':u'清华大学',
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
        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)', re.DOTALL),
        'encoding':'utf8',
        'rank':2,
    }; 

tjbbs = {
        'locate':'http://bbs.tongji.edu.cn/rssi.php?h=1',
        'root':'',
        'bbsname':'tongji',
        'schoolname':u'同济大学',
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
        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)', re.DOTALL),
        'encoding':'utf8',
        'rank':25,
    }; 
    
lilybbs = {
        'locate':'http://bbs.nju.edu.cn/bbstop10',
        'root':'http://bbs.nju.edu.cn/',
        'xpath':'/html/center/table',
        'bbsname':'lily',
        'schoolname':u'南京大学',
        'chinesename':u'小百合',
        'dom_row_pattern' : """
            <tr>
            <td>*
            <td><a href="$boardlink">$board</a>
            <td><a href="$titlelink">$title</a>
            <td><a href="$authorlink">$author</a>
            <td>$postcount
        """,
        're_block':re.compile(r'<table width=640>.*?</table>', re.DOTALL),
        'rank':5,
    };
    
zjubbs = {
        'locate':'http://www.freecity.cn/agent/top10.do',
        'root':'http://www.freecity.cn/agent/',
        'bbsname':'zju',
        'schoolname':u'浙江大学',
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
        're_block':re.compile(r'<table .*?>.*?</table>', re.DOTALL),
        'rank':4,
        
    };
    
fudanbbs = {
        'locate':'http://bbs.fudan.edu.cn/cgi-bin/bbs/bbstop10',
        'root':'http://bbs.fudan.edu.cn/cgi-bin/bbs/',
        'xpath':'/html/center/table/tr[2]/td[2]/table',
        'bbsname':'fudan',
        'schoolname':u'复旦大学',
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
        're_block':re.compile(r'<table border=0 width=100%>.*?</table>', re.DOTALL),
        'rank':6,
    };
    

    
    
xjtubbs = {
        'locate':'http://bbs.xjtu.edu.cn/BMYELAVBXDPIOAJBDICRKENIKWXEIKSVQZJU_B/bbstop10',
        'root':'http://bbs.xjtu.edu.cn/BMYELAVBXDPIOAJBDICRKENIKWXEIKSVQZJU_B/',
        'xpath':'/body/center/table',
        'bbsname':'xjtu',
        'schoolname':u'西安交通大学',
        'chinesename':u'兵马俑',
        'dom_row_pattern' : """
            <tr>
            <td>*</td>
            <td><a href="$boardlink">$board</a></td>
            <td><a href="$titlelink">$title</a></td>
            <td>$postcount</td>
            </tr>
        """,
        're_block':re.compile(r'<table border=1>.*?</table>', re.DOTALL),
        'rank':12,

    };
whubbs = {
        'locate':'http://bbs.whu.edu.cn/rssi.php?h=1',
        'root':'',
        'xpath':'/html/body/div[2]/table/tr/td/fieldset',
        'bbsname':'whu',
        'schoolname':u'武汉大学',
        'chinesename':u'珞珈山水',
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
        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)', re.DOTALL),
        'encoding':'utf8',
        'rank':10,

    };
    
xmubbs = {
        'locate':'http://bbs.xmu.edu.cn/mainpage.php',
        'root':'http://bbs.xmu.edu.cn/',
        'bbsname':'xmu',
        'schoolname':u'厦门大学',
        'chinesename':u'鼓浪听涛',
        'xpath':'/html/body/table[2]/tr/td/table[3]',
        'dom_row_pattern' : """
        <tr>
        <td>
        *
        <a href="$boardlink">$board</a>
        *
        <a href="$titlelink">$title</a>
        </td>
        <td>
        <a href="$authorlink">$author</a>
        *
        </td>
        </tr>
        """,
#        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
#        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)', re.DOTALL),
#        'encoding':'utf8',
        'rank':23,
        'needXpath':True,
    }; 
    
    
ustcbbs = {
        'locate':'http://bbs.ustc.edu.cn/cgi/bbstop10',
        'root':'http://bbs.ustc.edu.cn/cgi/',
        'xpath':'/html/center/table',
        'bbsname':'ustc',
        'schoolname':u'中国科学技术大学',
        'chinesename':u'瀚海星云',
        'dom_row_pattern' : """
            <tr>
            <td>*
            <td><a href="$boardlink">$board</a>
            <td><a href="$titlelink">$title</a>
            <td><a href="$authorlink">$author</a>
            <td>$postcount
        """,
        're_block':re.compile(r'<table border=0 width=90%>.*?</table>', re.DOTALL),
        'rank':7,
        
    };
    
sysubbs = {
        'locate':'http://bbs.sysu.edu.cn/bbstop10',
        'root':'http://bbs.sysu.edu.cn/',
        'bbsname':'sysu',
        'schoolname':u'中山大学',
        'chinesename':u'逸仙时空',
        'dom_row_pattern' : """
        <tr> 
        <td>*</td>
        <td>
        <a href="$boardlink">$board</a>
        </td>
        <td>
        <a href='$titlelink'>$title</a>
        </td>     
        <td>
        <a href="$authorlink">$author</a>
        </td>
        <td>$postcount</td>
        </tr>
        """,
        're_block':re.compile(r'<table width="100%" border="0" cellspacing="0" cellpadding="0" height="">.*?</table>', re.DOTALL),
        'rank':8,
        
    };
    
dlutbbs = {
        'locate':'http://bbs.dlut.edu.cn/rssi.php?h=1',
        'root':'',
        'bbsname':'dlut',
        'schoolname':u'大连理工大学',
        'chinesename':u'碧海青天',
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
        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)', re.DOTALL),
        'encoding':'utf8',
        'rank':24,
    }; 

njuptbbs = {
        'locate':'http://bbs.njupt.edu.cn/cgi-bin/bbstop10',
        'root':'http://bbs.njupt.edu.cn/cgi-bin/',
        'bbsname':'njupt',
        'schoolname':u'南京邮电大学',
        'chinesename':u'紫金飞鸿',
        'dom_row_pattern' : """
            <tr>
            <td>*
            <td><a href="$boardlink">$board</a>
            <td><a href="$titlelink">$title</a>
            <td><a href="$authorlink">$author</a>
            <td>$postcount
        """,
        're_block':re.compile(r'<table border=1 width=610>.*?</table>', re.DOTALL),
        'rank':13,
        
    };
    
csubbs = {
        'locate':'http://bbs.csu.edu.cn/top10_rss.xml',
        'root':'',
        'bbsname':'csu',
        'schoolname':u'中南大学',
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
        're_block':re.compile(r'<rdf:RDF.*?>.*?</rdf:RDF>', re.DOTALL),
        're_board1':re.compile(r'board=(?P<board>.*?)&', re.DOTALL),
        'rank':19,
    }; 

jlubbs = {
        'locate':'http://bbs.jlu.edu.cn/cgi-bin/bbssec',
        'root':'http://bbs.jlu.edu.cn/cgi-bin/',
        'xpath':'/html/body/table/tr/td/table/tr[4]/td/table/tr/td[2]/table',
        'bbsname':'jlu',
        'schoolname':u'吉林大学',
        'chinesename':u'牡丹园',
        'dom_row_pattern' : """
            <tr>
            <td>◆<a href="$titlelink">$title</a>
            </td>
            </tr>   
        """,
        #'re_block':re.compile(r'<legend>今日推荐精彩话题</legend><ul>.*?</ul>',re.DOTALL),
        're_board1':re.compile(r'board=(?P<board>.*?)&', re.DOTALL),
        'rank':11,
        'needXpath':True,

    };
    
bjtubbs = {
        'locate':'http://forum.byr.edu.cn/wForum/index.php',
        'root':'http://forum.byr.edu.cn/wForum/',
        'bbsname':'bjtu',
        'schoolname':u'北京邮电大学',
        'chinesename':u'北邮人',
        'dom_row_pattern' : """
            <a href="$titlelink">$title</a>
            *
            <font color="red">$postcount</font>
            *
            <br> """,
        're_block':re.compile(r'<thead><tr><th height="25"=100%>.{18}</td></tr></thead>.*?</table>', re.DOTALL),
        're_board1':re.compile(r'board.*?=(?P<board>.*?)&', re.DOTALL),
        'rank':13,

    };

rucbbs = {
        'locate':'http://bbs.ruc.edu.cn/wForum/topten.php',
        'root':'http://bbs.ruc.edu.cn/wForum/',
        'bbsname':'ruc',
        'schoolname':u'中国人民大学',
        'chinesename':u'天地人大',
        'xpath':'/html/body/table[4]',
        'dom_row_pattern' : """
            <tr>
            <td>*</td>
            <td>&nbsp;<a href="$boardlink">$board</a></td>
            <td>&nbsp;<a href="$titlelink">$title</a></td>
            <td><a href="$authorlink">$author</a></td>
            <td>&nbsp;$postcount</td>
            </tr>
        """,
        #'re_block':re.compile(r'<thead><tr><th height="25"=100%>.{18}</td></tr></thead>.*?</table>', re.DOTALL),
        'rank':21,
        'needXpath':True,
    }  ; 
seubbs = {
        'locate':'http://bbs.seu.edu.cn/mainpage.php',
        'root':'http://bbs.seu.edu.cn/',
        'bbsname':'seu',
        'schoolname':u'东南大学',
        'chinesename':u'虎踞龙蟠',
        'xpath':'/html/body/div[4]/div[2]/div[3]',
        'dom_row_pattern' : """
        <li>
        <a href="$titlelink">$title</a>
        </li>
        """,
        're_board1':re.compile(r'board.*?=(?P<board>.*?)&', re.DOTALL),
        'rank':20,
        'needXpath':True,
    }  ;

scubbs = {
        'locate':'http://bbs.scu.edu.cn/rssi.php?h=1',
        'root':'',
        'bbsname':'scu',
        'schoolname':u'四川大学',
        'chinesename':u'蓝色星空',
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
        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)', re.DOTALL),
        'encoding':'utf8',
        'rank':12,
    }; 

hitbbs = {
        'locate':'http://www.lilacbbs.com/rssi.php?h=1',
        'root':'',
        'bbsname':'hit',
        'schoolname':u'哈尔滨工业大学',
        'chinesename':u'紫丁香社区',
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
        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)', re.DOTALL),
        'encoding':'utf8',
        'rank':14,
    }; 

sdubbs = {
        'locate':'http://bbs.sdu.edu.cn/mainpageblue.php',
        'root':'http://bbs.sdu.edu.cn',
        'bbsname':'sdu',
        'schoolname':u'山东大学',
        'chinesename':u'泉韵心声',
        'xpath':'/html/body/div/table[2]/tr[2]/td/table[2]/tr/td',
        'dom_row_pattern' : """
        <li>
        <a href="$titlelink">$title</a>
        *
        <a href="$authorlink">$author</a>
        *
        <a href="$boardlink">$board</a>
        *
        </li>
        """,
        'rank':16,
        'needXpath':True,
    }  ;


tjubbs = {
        'locate':'http://bbs.tju.edu.cn/TJUBBSFPKEHPUMNSALVFGWTYHVMRLBXCBIYPKFA_A/bbstop10',
        'root':'http://bbs.tju.edu.cn/TJUBBSFPKEHPUMNSALVFGWTYHVMRLBXCBIYPKFA_A/',
        'bbsname':'tju',
        'schoolname':u'天津大学',
        'chinesename':u'天大求实',
        'dom_row_pattern' : """
        <tr>
        <td>*</td>
        <td>
        <a href='$boardlink'>$board</a>
        </td>
        <td>
        <a href='$titlelink'>$title</a>
        </td>
        <td>$postcount</td>
        </tr>
        """,
        're_block':re.compile(r'<table class=tb3>.*?</table>', re.DOTALL),
        'rank':18,
           }  ;

buaabbs = {
        'locate':'http://bbs.buaa.edu.cn/mainpage.php',
        'root':'http://bbs.buaa.edu.cn',
        'bbsname':'buaa',
        'schoolname':u'北京航空航天大学',
        'chinesename':u'未来花园',
        'dom_row_pattern' : """
        <li>
        <a href="$titlelink">$title</a>
        * 
        <a href="$authorlink">$author</a>
        *
        <a href="$boardlink">$board</a>
        *
        </li>
        """,
        're_block':re.compile(r'<td class="MainContentText">.*?</td>', re.DOTALL),
        'rank':22,
           }  ;

 

lzubbs = {
        'locate':'http://bbs.lzu.edu.cn/mainpage.php',
        'root':'http://bbs.lzu.edu.cn/',
        'bbsname':'lzu',
        'schoolname':u'兰州大学',
        'chinesename':u'西北望',
        'xpath':'/html/body/table[3]/tr[2]/td/table[2]/tr/td/table/tr',
        'dom_row_pattern' : """
        <li>
        [<a href="$boardlink">$board</a>]
        <a href="$titlelink">$title</a>
        *
        <a href="$authorlink">$author</a>
        *
        </li>
        """,
        'rank':28,
        'needXpath':True,
    }  ;

caubbs = {
        'locate':'http://wusetu.cn/WSTAMnACUKGSZERBGBTWPARKFXGTBPZIFMVFLTVK_A/bbsboa?secstr=?',
        'root':'http://wusetu.cn/WSTAMnACUKGSZERBGBTWPARKFXGTBPZIFMVFLTVK_A/',
        'bbsname':'cau',
        'schoolname':u'中国农业大学',
        'chinesename':u'五色土',
        'xpath':'/html/body/tr[7]/td',
        'dom_row_pattern' : """
        <tr>
        <td>
        <a href='$boardlink'>$board</a>
        </td>
        <td>
        <a href='$titlelink'>$title</a>
        </td>
        <td>
        *
        </td>
        <td>
        <a href='$authorlink'>$author</a>
        </td>
        <td>
        </td>
        </tr>
        """,
        'rank':32,
        'needXpath':True,
    }  ;



ustbbbs = {
        'locate':'http://bbs.ustb.edu.cn/mainpage.php',
        'root':'http://bbs.ustb.edu.cn/',
        'bbsname':'ustb',
        'schoolname':u'北京科技大学',
        'chinesename':u'幻想空间',
        'xpath':'/html/body/table[3]/tr[2]/td/p/table[4]',
        'dom_row_pattern' : """
        <tr>
        <td>
        *
        <a href="$boardlink">$board</a>
        *
        <a href="$titlelink">$title</a>
        </td>
        <td>
        <a href="$authorlink">$author</a>
        *
        </td>
        </tr>
        """,
        'rank':42,
           }  ;
           
uestcbbs = {
        'locate':'http://bbs.uestc.edu.cn/cgi-bin/bbstop10',
        'root':'http://bbs.uestc.edu.cn/cgi-bin/',
        'bbsname':'uestc',
        'schoolname':u'电子科技大学',
        'chinesename':u'一往情深',
        'xpath':'/html/table',
        'dom_row_pattern' : """
        <tr>
        <td>*</td>
        <td>
        <a href="$boardlink">$board</a>
        </td>
        <td>
        <a href="$titlelink">$title</a>
        </td>
        <td>
        <a href="$authorlink">$author</a>
        </td>
        <td>$postcount</td>
        </tr>
        """,
        'rank':43,
           }  ;
