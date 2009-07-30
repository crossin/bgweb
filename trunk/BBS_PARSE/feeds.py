from django.contrib.syndication.feeds import Feed 
from django.utils.feedgenerator import Atom1Feed 
from model.models import *;
from django.utils.feedgenerator import Rss201rev2Feed
from django.http import *
 
class RssSiteContentFeed(Feed): 
  title = "helloworld" 
  link = "http://www.game13.net/content/list/" 
  description = "game video game info ;" 
 
  items = ('Item 1', 'Item 2')
 
class AtomSiteContentFeed(RssSiteContentFeed): 
  feed_type = Atom1Feed 
  subtitle = RssSiteContentFeed.description 
  
  


def rss201(request):
    try:
         highschoollist = HighSchoolBbs.all().order('rank')[:10];
    except:
        raise Http404
    current_site = 'localhost';
    blog_link = u'http://%s/blog/' % 'bbs10'
    feed = Rss201rev2Feed( u"I Can't Believe It's Blog!", blog_link,
        u'The Great Example of Why 99.999% of Blogs Suck' )
    for object in highschoollist:
        author = object.schoolname;
        link = blog_link + object.schoolname
        feed.add_item( object.chinesename.encode('utf-8'), link, object.schoolname.encode('utf-8'), 
            author_email=author.encode('utf-8'), author_name=author.encode('utf-8'), 
            unique_id=link,
            categories=[] )
    response = HttpResponse(mimetype='application/xml')
    feed.write(response, 'utf-8')
    return response

