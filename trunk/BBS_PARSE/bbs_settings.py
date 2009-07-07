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
        're_block':re.compile(r'<ul id="toptenlist">.*?</ul>', re.DOTALL),
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
        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)', re.DOTALL),
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
        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
        're_board':re.compile(r'\[(?P<board>.*?)\] (?P<title>.*)', re.DOTALL),
        'encoding':'utf8',
        'rank':25,
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
        're_block':re.compile(r'<table width=640>.*?</table>', re.DOTALL),
        'rank':5,
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
        're_block':re.compile(r'<table .*?>.*?</table>', re.DOTALL),
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
        're_block':re.compile(r'<table border=0 width=100%>.*?</table>', re.DOTALL),
        'rank':6,
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
        're_block':re.compile(r'<table .*?>.*?</table>', re.DOTALL | re.I),
        'rank':15,
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
        're_block':re.compile(r'<table border=1>.*?</table>', re.DOTALL),
        'rank':12,

    };
whubbs = {
        'locate':'http://bbs.whu.edu.cn/rssi.php?h=1',
        'root':'',
        'xpath':'/html/body/div[2]/table/tr/td/fieldset',
        'name':'whu',
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
        'name':'xmu',
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
        're_block':re.compile(r'<table border=0 width=90%>.*?</table>', re.DOTALL),
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
        're_block':re.compile(r'<div id="topten">.*?</div>', re.DOTALL),
        'rank':8,
        
    };
    
dlutbbs = {
        'locate':'http://bbs.dlut.edu.cn/rssi.php?h=1',
        'root':'',
        'name':'dlut',
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
        're_block':re.compile(r'<table border=1 width=610>.*?</table>', re.DOTALL),
        'rank':20,
        
    };
    
csubbs = {
        'locate':'http://bbs.csu.edu.cn/top10_rss.xml',
        'root':'',
        'name':'csu',
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
        'name':'jlu',
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

    };
    
bjtubbs = {
        'locate':'http://forum.byr.edu.cn/wForum/index.php',
        'root':'http://forum.byr.edu.cn/wForum/',
        'name':'bjtu',
        'chinesename':u'北邮人',
        'dom_row_pattern' : """
            <a href="$titlelink">$title</a>
            *
            <font color="red">$postcount</font>
            *
            <br> """,
        're_block':re.compile(r'<thead><tr><th height="25"=100%>.{18}</td></tr></thead>.*?</table>', re.DOTALL),
        're_board1':re.compile(r'board.*?=(?P<board>.*?)&', re.DOTALL),
        'rank':20,

    };

rucbbs = {
        'locate':'http://bbs.ruc.edu.cn/wForum/topten.php',
        'root':'http://bbs.ruc.edu.cn/wForum/',
        'name':'ruc',
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
           }  ; 
seubbs = {
        'locate':'http://bbs.seu.edu.cn/mainpage.php',
        'root':'http://bbs.seu.edu.cn/',
        'name':'seu',
        'chinesename':u'虎踞龙蟠',
        'xpath':'/html/body/div[4]/div[2]/div[3]',
        'dom_row_pattern' : """
        <li>
        <a href="$titlelink">$title</a>
        </li>
        """,
        're_board1':re.compile(r'board.*?=(?P<board>.*?)&', re.DOTALL),
        'rank':20,
           }  ;
ecnubbs = {
        'locate':'http://bbs.iecnu.com/',
        'root':'http://bbs.iecnu.com/',
        'name':'ecnu',
        'chinesename':u'爱在华师大',
        'xpath':'/html/body/div[8]/table/tr[2]/td[3]/table/tr/td[2]',
        'dom_row_pattern' : """
        <div>
        <a href="$titlelink">$title</a>
        </div>
        """,
        'rank':30,
           }  ;
scubbs = {
        'locate':'http://bbs.scu.edu.cn/rssi.php?h=1',
        'root':'',
        'name':'scu',
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
        'rank':13,
    }; 

hitbbs = {
        'locate':'http://www.lilacbbs.com/rssi.php?h=1',
        'root':'',
        'name':'hit',
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
        'name':'sdu',
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
           }  ;
bnubbs = {
        'locate':'http://bbs.bnulife.com/index.php',
        'root':'http://bbs.bnulife.com/',
        'name':'bnu',
        'chinesename':u'紫金香',
        'dom_row_pattern' : """
        <div>
        <img/> 
        <a href="$titlelink">$title</a>
        </div>
        """,
        're_block':re.compile(r'<div id="weeks2">.*?</div></div>', re.DOTALL),
        'rank':17,
    }; 

tjubbs = {
        'locate':'http://bbs.tju.edu.cn/TJUBBSFPKEHPUMNSALVFGWTYHVMRLBXCBIYPKFA_A/bbstop10',
        'root':'http://bbs.tju.edu.cn/TJUBBSFPKEHPUMNSALVFGWTYHVMRLBXCBIYPKFA_A/',
        'name':'tju',
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
        'name':'buaa',
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

scutbbs = {
        'locate':'http://bbs.scut.edu.cn/rss/ListTopTen.jsp',
        'root':'',
        'name':'scut',
        'chinesename':u'木棉',
        'dom_row_pattern' : """
            <item>
            <title>$title</title>
            <link>$titlelink</link>
            <author>$author</author>
            <guid>$boardlink</guid>
            <description>*</description>
            <pubDate>*</pubDate>
            <category>*</category>
            </item>
        """,
        're_block':re.compile(r'<rss version="2.0">.*?</rss>', re.DOTALL),
        'encoding':'utf8',
        'rank':26,
    }; 

lzubbs = {
        'locate':'http://bbs.lzu.edu.cn/mainpage.php',
        'root':'http://bbs.lzu.edu.cn/',
        'name':'lzu',
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
           }  ;

caubbs = {
        'locate':'http://wusetu.cn/WSTAMnACUKGSZERBGBTWPARKFXGTBPZIFMVFLTVK_A/bbsboa?secstr=?',
        'root':'http://wusetu.cn/WSTAMnACUKGSZERBGBTWPARKFXGTBPZIFMVFLTVK_A/',
        'name':'cau',
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
           }  ;

shubbs = {
        'locate':'http://bbs.lehu.shu.edu.cn/',
        'root':'',
        'name':'shu',
        'chinesename':u'乐乎论坛',
        'xpath':'/html/body/div[2]/div[3]/div[5]/div[2]',
        'dom_row_pattern' : """
        <li>
        <a href="$titlelink">$title</a>
        </li>
        """,
        'encoding':'utf8',
        'rank':41,
           }  ;

ustbbbs = {
        'locate':'http://bbs.ustb.edu.cn/mainpage.php',
        'root':'http://bbs.ustb.edu.cn/',
        'name':'ustb',
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
        'name':'uestc',
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
