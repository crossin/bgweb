bbs sites constantly update their doms ( because their site engine or structure is that poor )
this is some steps we do to fix the site change today


# Introduction #
**PY FILE GOES HERE**

"""
#PATCH ON SJTU V2 - lefted guidance
#GET PATTERN LINE USING REPR
#PRINCIPAL NO.1 YOU CAN FORMAT THE DOM WHEN YOU OBSERVE,BUT WHEN YOU HANLE IT TO MACHINE, PLEASE KEEP IT 

&lt;B&gt;

ORGINAL

&lt;/B&gt;



pattern =
htmlstring = urllib2.urlopen('http://bbs.sjtu.edu.cn/php/bbsindex.html').read();
htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');
blockstring = re.search(pattern,htmlstring,re.DOTALL).group();
print blockstring;
"""
##PATCH ON FDU V2
url = "http://www.lilacbbs.com/"
#PRINCIPAL NO.2 YOU MAY NEED DOM STRUCTURE TO HELP YOU DETERMINE RE EXPRESSION"
pattern = """"""
htmlstring = urllib2.urlopen(url).read();
htmlstring = unicode(htmlstring, 'GBK', 'ignore').encode('UTF-8');

blockstring = re.search(pattern,htmlstring,re.DOTALL).group();
print blockstring;

# Details #

**the fix details goes here and large html content are simply neglected**

`
#new problems broughted about
1. scraped infomation are seemingly more instructed, info structure should be improved or restructure or abstracted
-->stormed: store these infomation in serialized dict would be better choice, missed keys could be restored by default values.
-->integrated with site framework redone. maybe in the next two versions.
2. the parser engine should be improved to report site structure changes(only structure change) and site inavailabe for long time.
!important.