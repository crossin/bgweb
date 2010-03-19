# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string

from django.utils.translation import ugettext as _
from django.utils import simplejson

from google.appengine.ext import db
from google.appengine.api import users
from ragendja.dbutils import *;
from django.shortcuts import render_to_response as rtr;
from ragendja.mrender import render_to_response as rtrg;
from content.models import *;

from form import *;
from decorators import *;

from pageharvest.settings import *;
from pageharvest.bbs_parser import BBSParser;
from datetime import *;
import time;


from pageharvest.settings   import *;
from content.decorators import *;





PAGE_SIZE = 20;
PAGES_TO_LIST = 10;
USER_QUOTA = 100;
def searchlinksbypost( request, tagname="", pagenumber=0, template='search-template.html', extra_context=None):
    if request.method == 'POST':
        tagname = request.POST['tagname'];
        return  HttpResponseRedirect(reverse('searchlistbytag', args=[tagname,0]))
    else:
        return HttpResponseRedirect(reverse('content_home'))

def searchlinksbytag( request, tagname="", pagenumber=0, template='search-template.html', extra_context=None):     
    context = RequestContext(request);

    if( tagname =="" ):
        context['has_error'] = True;
        context['info'] = u'空白关键字搜索 ';
        return rtr( template, context, context_instance=extra_context);
    elif( tagname == u"十大收录" ):
        context['has_error'] = True;
        context['info'] = u'大部分帖子都有这个标签,直接按列表查看 ';
        return rtr( template, context, context_instance=extra_context);
    q = LinkTags.all().filter('name =', tagname );
    if( q.count() == 0 ):
        context['has_error'] = True;
        context['info'] = u'没有与这个标签相关的帖子 ';
        return rtr( template, context, context_instance=extra_context);
        
    try:
        q = paginate(q,int(pagenumber),context);
    except Exception, e:
        pass;

    link_keys  = [LinkTags.link.get_value_for_datastore(Link) for Link in q]
    links      = db.get(link_keys)
    schoolkeys  = [Bbslinks.school.get_value_for_datastore(Link) for Link in links]
    schools     = db.get(schoolkeys)
    for link,school in zip(links,schools):
        link.pschool = school;
    context['linklist'] = links;
    context['has_error'] = False;
    return rtr( template, context, context_instance=extra_context)

def viewbylinks( request, pagenumber=0, template='bbs-template.html', extra_context=None):
             
    context = RequestContext(request);
    
    object_query = Bbslinks.all()
    #object_query = get_object_list(Bbslinks);
    try:
        object_list = paginate(object_query,int(pagenumber),context);
    except Exception, e:
        pass;
    
    schoolkeys  = [Bbslinks.school.get_value_for_datastore(Link) for Link in object_list]
    schools     = db.get(schoolkeys)
    for link,school in zip(object_list,schools):
        link.pschool = school;
    context['linklist'] = object_list;

    return rtr( template, context, context_instance=extra_context)
    
def getBbsListBySchool(bbsname):
    try:
        school = get_object(Schoolbbs, 'bbsname =' , bbsname);
    except Exception,e:
        #print 'no school with bbsname:', bbsname;
        return;

    #toptenlist = Bbslinks.gql('where school = :1 ORDER BY order ASC', school);
    toptenlist = get_object_list( Bbslinks, 'school =', school );
    #print school.schoolname;
    bbsinfo = {
                'schoolname':         (school.schoolname),
                'chinesename':  (school.chinesename),
                'itemlist':     toptenlist.order( '-updatetime' ).fetch(10),
    }
    return bbsinfo;

def viewxnhome(request, pagenumber=0, template='content_by_school.html', extra_context=None):
    context = RequestContext(request); 
    bbsnamelist = [];
    pclist  = ParseConfig.all().filter( ' status = ', STATUS_NORMAL );
    
    try:
        pclist = paginateschoolconfig(pclist,int(pagenumber),context,5);
    except Exception, e:
        pass;
    
    for item in pclist:
        bbsnamelist.append(item.school.bbsname);
        
    bbslist = [];
    for name in  bbsnamelist:
        bbslist.append(getBbsListBySchool(name));
        
    context['list'] = bbslist;
        
    return rtr(template, context,extra_context);
    
def viewbyschool(request, template='content_by_school.html', extra_context=None):
    context = RequestContext(request); 
    bbsnamelist = [];

    pclist = ParseConfig.all().filter( 'status = ', STATUS_NORMAL ).order( 'rank' );
    
    for item in pclist:
        bbsnamelist.append(item.school.bbsname);
     
            
    bbslist = [];
    for name in  bbsnamelist:
        bbslist.append(getBbsListBySchool(name));

   
    length = len( bbslist );
    context['col1'] = bbslist[0:length/2];
    context['col2'] = bbslist[length/2 + 1 : length ];
    
    recommendlist = Bbslinks.all().filter( 'source =', 'recommend' ).order('-updatetime').fetch(10);
    context['recommend'] = recommendlist;
    qann  = Announcement.all();
    if( qann.count() == 0 ): context['announcement'] = "Currently No Announcement";
    else:context['announcement'] = qann.fetch(1)[0];
    #context['announcement'] = ann;
    context_instance=RequestContext(request)
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);
    
def viewframedcontent(request, template='framed_link_content.html', extra_context=None):
    context = RequestContext(request);
   
    linkid = request.GET.get('linkid', '');#TODO:EXCEPTION HANDLING
    linkitem = db.get( linkid );
    context['link'] = linkitem;
    #print linkitem.titlelink;
    linkitem.visitcount = linkitem.visitcount + 1;
    linkitem.put();
    
    available_tags = MTags.all();
    context['all_tags'] = available_tags;
    context['is_user'] = is_bt_user(request);
    
    context_instance=RequestContext(request);
    context_instance.autoescape=False;

    return rtrg(template, context,context_instance);

def viewaccount( request, template='account_interface.html', extra_context=None):
    context = RequestContext(request);
    q = UserAccount.all();
    context['hasquota'] = q.count() < USER_QUOTA;
    context['acount_left'] = USER_QUOTA - q.count();
    return rtr(template, context,extra_context);


# OPERATION VIEWS THROUGH AJAX CALLS
@bt_user_only
def tagginglinks(request, template='tagging.json', extra_context=None):
    context = {};
    tag_name = request.POST['tagname'];
    linkid = request.POST['linkid'];
    valid_link = tag_name != None and linkid != None; # tag name in my list
    #or user == None or not users.is_current_user_admin()
    if( not valid_link  ):
        context['result'] = 0;
        return rtr(template, context,extra_context);
    
    linkitem = db.get(linkid);
    try:
        linkitem.tags.index( tag_name );
    except Exception, e:
        linkitem.tags.append( tag_name );
    linkitem.put();
    lt = LinkTags( link = linkitem, name = tag_name );
    lt.put();
    
    context['result'] = 1; 
    return rtr(template, context,extra_context);

SUPPORT = 1;
DOWN    = 2;
def ratinglinks(request, template='tagging.json', extra_context=None):    
    context={};
    linkid = request.POST['linkid'];
    operate_id = int ( request.POST['opid'] );
    valid_link = operate_id != None and linkid != None;
    
    if( not valid_link  ):
        context['result'] = 0;
        context['info']   =u'链接并不正确';
        return HttpResponse( simplejson.dumps(context,ensure_ascii = False) );
    
    linkitem = db.get(linkid);
    if (    operate_id == SUPPORT ):
        linkitem.supportcount = linkitem.supportcount+1;
    elif (  operate_id == DOWN ):
        linkitem.objectcount = linkitem.objectcount + 1;
    linkitem.put();
    context['result'] = 1; 
    return HttpResponse( simplejson.dumps(context,ensure_ascii = False) );

def getcomments(request, template='comment.html', extra_context=None):
    context = {};extra_context={};
    linkid = request.POST['linkid'];
    valid_link =  linkid != None;
    
    if( not valid_link  ):
        context['result'] = 0;
        context['info']   =u'链接并不正确';
        return HttpResponse( simplejson.dumps(context,ensure_ascii = False) );
    comments = Comment.all().filter( 'link = ', db.Key(linkid) );
    count = comments.count();
    if( count == 0 ): 
        context['info'] = u'目前还没有评论';
        context['error'] = True;
    else:
        context['error'] = False;
        

    extra_context['comments'] = comments.fetch(count);
    context['html']     = render_to_string('comment.html', extra_context);
    context['cmtcount'] =  count;
    return HttpResponse( simplejson.dumps(context,ensure_ascii = False) );
    

def commentlink(request, template='tagging.json', extra_context=None):
    context = {};
    linkid = request.POST['linkid'];
    cmtbody= request.POST['comment'];
    valid_link = cmtbody != None and linkid != None;
    
    if( not valid_link  ):
        context['result'] = 0;
        return rtr(template, context,extra_context);
    
    if( len(cmtbody) >= 100 ):
        cmtbody = cmtbody[0:50];
    
    linkitem = db.get(linkid);
    Comment( body = cmtbody , link = linkitem ).put();
    linkitem.commentcount = linkitem.commentcount + 1;
    linkitem.put();
    context['result'] = 1; 
    return rtr(template, context,extra_context);

@bt_user_only
def addtag(request, template='tagging.json', extra_context=None):
    return ajax_operation( MTagsForm, request, template, extra_context );

@bt_user_only
def addlink(request, template='result.json', extra_context=None):
    return ajax_operation( LinkForm, request, template, extra_context );


def addaccount(request, template='result.json', extra_context=None):
    return ajax_operation( AccountForm, request, template, extra_context );
    
@admin_user_only  
def addannouncement(request, template='result.json', extra_context=None):
    return ajax_operation( AnnouncementForm, request, template, extra_context );

@bt_user_only
def manangement(request, template='admin_interface.html', extra_context=None):
    context = RequestContext(request);
    tags = MTags.all().fetch(1000);
    context['tags'] = tags;
    context['isadmin'] = users.is_current_user_admin();
    
    return rtr(template, context,extra_context);


parser = BBSParser();
@admin_user_only 
def gae_cron_job_parse( request , template='cron_result.html',extra_context=None):
    context=RequestContext(request);
    now         = datetime.now()
    delta       = timedelta( minutes = -40 );
    criteria    = now + delta;

    not_updated_list = get_object_list(ParseConfig, 'lastfresh < ', criteria, ' status =  ', STATUS_NORMAL );
    context['not_updated_count'] = len( not_updated_list );
    finished_name_list = [];
    duration = 0;
    for bbs_config in not_updated_list:
        #t1 = time.time();
        parsetime = parser.parsebbs( bbs_config.toDict(), bbs_config );
        #t2 = time.time();
        finished_name_list.append( bbs_config.school.chinesename );
        duration += parsetime;
        if duration > parse_time_limit:
            break;
    context['updated_count'] = len( finished_name_list );
    context['finished_names'] = finished_name_list;
    context['duration'] = duration;
    context_instance=RequestContext(request);
    return render_to_response(template, context,context_instance);


@admin_user_only 
def gae_setup_initial_data( request , template='cron_result.html',extra_context=None):
    from content.models         import *;
    from pageharvest.settings   import *;
    for bc in bbs_setting_list :
            item = get_object(Schoolbbs,  'schoolname =',  bc['schoolname'] );
            if not item :
                now = datetime.now();
                school = db_create( Schoolbbs, lastfresh = now, **bc );
                if( bc['bbsname'] != 'recommend' ):
                    config = db_create( ParseConfig,  school = school, **bc );
                
    return HttpResponse('All School data setup successfully');

#Util method defined to help with pagination links
def paginate( query, page_number , context, pagesize = PAGE_SIZE ):
    global  PAGES_TO_LIST;
    total_items = query.count();
    total_pages = total_items / pagesize;

    
    if( page_number < 0 or page_number > total_pages ):
        context['info'] = 'Invalid Page Number ';
        raise Exception('Invalid Page Number');
    
    if( total_pages < PAGES_TO_LIST ): page_range = total_pages;
    else: page_range = PAGES_TO_LIST;
    
    context['current_page'] = page_number;
    context['total_page']   = total_pages;
    if( page_number > 0 ): 
        context['has_previous'] = True;
        context['previous_page'] = page_number -1;
    else: context['has_previous'] = False;
    
    if( page_number < total_pages ):
        context['has_next'] = True;
        context['next_page'] = page_number +1;
    else: context['has_next'] = False;
        
    start_index = max(0,page_number - page_range/2);
    end_index = min(total_pages,start_index+page_range);
        
    context['page_range'] = range( start_index, end_index+1 );
    
    
    result_link_page = query.order('-updatetime').fetch( (page_number+1)*pagesize, page_number*pagesize );
    if( len(result_link_page) > pagesize ):
        result_link_page = result_link_page[0:pagesize];
    return result_link_page;

def paginateschoolconfig( query, page_number , context, pagesize = PAGE_SIZE ):
    global  PAGES_TO_LIST;
    total_items = query.count();
    total_pages = total_items / pagesize;

    
    if( page_number < 0 or page_number > total_pages ):
        context['info'] = 'Invalid Page Number ';
        raise Exception('Invalid Page Number');
    
    if( total_pages < PAGES_TO_LIST ): page_range = total_pages;
    else: page_range = PAGES_TO_LIST;
    
    context['current_page'] = page_number;
    context['total_page']   = total_pages;
    if( page_number > 0 ): 
        context['has_previous'] = True;
        context['previous_page'] = page_number -1;
    else: context['has_previous'] = False;
    
    if( page_number < total_pages ):
        context['has_next'] = True;
        context['next_page'] = page_number +1;
    else: context['has_next'] = False;
        
    start_index = max(0,page_number - page_range/2);
    end_index = min(total_pages,start_index+page_range);
        
    context['page_range'] = range( start_index, end_index+1 );
    
    
    result_link_page = query.order('rank').fetch( (page_number+1)*pagesize, page_number*pagesize );
    if( len(result_link_page) > pagesize ):
        result_link_page = result_link_page[0:pagesize];
    return result_link_page;


def ajax_operation(FORM_CLS, request, template='tagging.json', extra_context=None):
    context = {};
    if request.method == 'POST':
        form = FORM_CLS(request.POST);
        if( form.is_valid() ):
            form.save();
            context['result'] = 1;
        else:
            context['result'] = 0;
            context['info'] = form.getinfo();
    #return rtr(template, context,extra_context);
    return HttpResponse( simplejson.dumps(context,ensure_ascii = False) ); 
    