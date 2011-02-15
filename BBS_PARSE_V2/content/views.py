# -*- coding: utf-8 -*-
from datetime import *;
import time;
import random;
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils.translation import ugettext as _
from django.utils import simplejson
from django.shortcuts import render_to_response as rtr;

from google.appengine.ext import db
from google.appengine.api import users

from ragendja.dbutils import *;
from ragendja.mrender import render_to_response as rtrg;

from pageharvest.settings import *;
from pageharvest.bbs_parser import *;
from settings import *;

from models import *;
from decorators import *;
from form import *;

from adsys.decorators import random_record_xn_access;

    

def searchlinksbypost( request, tagname="", pagenumber=0, template='search-template.html', extra_context=None):
    if request.method == 'POST':
        tagname = request.POST['tagname'];
        return  HttpResponseRedirect(reverse('searchlistbytag', args=[tagname,0]))
    else:
        return HttpResponseRedirect(reverse('content_home'))

def searchlinksbytag( request, tagname="", pagenumber=0, template='search-template.html', extra_context=None):     
    context = RequestContext(request);
    if( tagname in SPECIAL_TAGS ):
        context['has_error'] = True;
        context['info'] = u'请在微博上FOLLOW -> CAMPUSNEWS 获取最新动态 ';
        return rtr( template, context, context_instance=extra_context);

    if( tagname =="" ):
        #context['has_error'] = True;
        #context['info'] = u'空白关键字搜索 ';
        #return rtr( template, context, context_instance=extra_context);
        raise;
    elif( tagname == u"十大收录" ):
        #context['has_error'] = True;
        #context['info'] = u'大部分帖子都有这个标签,直接按列表查看 ';
        #return rtr( template, context, context_instance=extra_context);
        return HttpResponseRedirect(reverse('content_list_home'))
    q = LinkTags.all().filter('name =', tagname );
    if( q.count() == 0 ):
        context['has_error'] = True;
        context['info'] = u'没有与这个标签相关的帖子 ';
        return rtr( template, context, context_instance=extra_context);
        
    try:
        global PAGE_SIZE;
        q = paginate(q,int(pagenumber),context, PAGE_SIZE, 'name' );
    except Exception, e:
        raise;

    link_keys  = [LinkTags.link.get_value_for_datastore(Link) for Link in q]
    links      = db.get(link_keys);
    schoolkeys  = [Bbslinks.school.get_value_for_datastore(Link) for Link in links]
    schools     = db.get(schoolkeys)
    for link,school in zip(links,schools):
        link.pschool = school;
    context['linklist'] = links;
    context['has_error'] = False;
    context_instance=RequestContext(request)
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);

def viewbylinks( request, pagenumber=0, template='bbs-template.html', extra_context=None):
    context = RequestContext(request);
    object_query = Bbslinks.all();
    try:
        object_list = paginate(object_query,int(pagenumber),context,PAGE_SIZE,"-visitcount" );
    except Exception, e:
        raise Http404;
    schoolkeys  = [Bbslinks.school.get_value_for_datastore(Link) for Link in object_list]
    try:
        schools = db.get(schoolkeys)
    except:
        raise Http404;
    for link,school in zip(object_list,schools):
        link.pschool = school;
    context['linklist'] = object_list;
    context_instance=RequestContext(request)
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);

#STRIP THE SPECICAL TAGS 
def processlinktag( link ):
    tags = link.tags;
    for tag in tags:
        if ( tag in SPECIAL_TAGS ): tags.remove( tag );
    
    tagcount = len(tags);
    link.hasxntag = True;
    if ( tagcount < 2 ):
        link.ptags = [];
        link.hasxntag = False;
        return;
    elif ( tagcount == 2 ):
        link.ptags = [ tags[1]];
    else:#tag count >=3
        rindex = random.randrange(2,tagcount);
        link.ptags = [ tags[1], tags[rindex] ];
        
def injectKeyName( link ):
    link.sid = link.key().id_or_name();
    
    
def getBbsListBySchool( bbsname, modification=False):
    try:
        school = get_object(Schoolbbs, 'bbsname =' , bbsname);
    except Exception,e:
        raise

    toptenlist = get_object_list( Bbslinks, 'school =', school );
    itemlist   = toptenlist.order( '-updatetime' ).fetch(10);
    if( modification ):#THIS FUNCTION IS REVISED FOR TAGGING IN XN PAGE
        for link in itemlist: processlinktag( link );
    for link in itemlist: injectKeyName( link );
    return {
        'schoolname': (school.schoolname),
        'chinesename':(school.chinesename),
        'itemlist':   itemlist,  
    }
@random_record_xn_access
def viewxnhome(request, pagenumber=0, template='content_by_school.html', extra_context=None):
    context = RequestContext(request); 
    bbsnamelist = [];
    pclist  = ParseConfig.all().filter( ' status = ', STATUS_NORMAL );
    try:
        pclist = paginateschoolconfig(pclist,int(pagenumber),context,5);
    except Exception, e:
        raise;
    for item in pclist:
        bbsnamelist.append(item.school.bbsname);
    bbslist = [];
    for name in  bbsnamelist:
        bbslist.append(getBbsListBySchool(name,True));
    context['list'] = bbslist;
    context_instance=RequestContext(request);
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);
    
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
    context['col2'] = bbslist[length/2  : length ];
    recommendlist = Bbslinks.all().filter( 'source =', 'recommend' ).order('-updatetime').fetch(10);
    context['recommend'] = recommendlist;
    qann  = Announcement.all();
    if( qann.count() == 0 ): context['announcement'] = "Currently No Announcement";
    else:context['announcement'] = qann.fetch(1)[0];
    context_instance=RequestContext(request)
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);
    
def view_parsing_status(request, template='school_status_list.html', extra_context=None):
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
    context['col2'] = bbslist[length/2  : length ];
    recommendlist = Bbslinks.all().filter( 'source =', 'recommend' ).order('-updatetime').fetch(10);
    context['recommend'] = recommendlist;
    qann  = Announcement.all();
    if( qann.count() == 0 ): context['announcement'] = "Currently No Announcement";
    else:context['announcement'] = qann.fetch(1)[0];
    
    schools = [];
    sq = Schoolbbs.all();
    for school in sq:
        try:
            pc = get_object( ParseConfig , 'school =', school );
            pc.__dict__['schoolname'] = school.schoolname; pc.__dict__['chinesename'] = school.chinesename;
            if ( pc.status != 1 ):
                pc.__dict__['normal'] = False;pc.__dict__['statusinfo']="ERROR";
            else: 
                pc.__dict__['normal'] = True;pc.__dict__['statusinfo']="NORMAL";
        except Exception,e:
            logging.error('school %s & parse config not consistent, detailed %s'%( school.bbsname,e));
            continue;
        schools.append(pc);
    context['schools'] = schools;context['count'] = len(schools);
    context_instance=RequestContext(request);
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);
    
def viewframedcontent(request, template='framed_link_content.html', extra_context=None):
    context = RequestContext(request);
    linkid = request.GET.get('linkid', '');#TODO:EXCEPTION HANDLING

    linkitem = get_object_or_404(Bbslinks,linkid);
    context['link'] = linkitem;
    linkitem.visitcount = linkitem.visitcount + 1;
    linkitem.put();
    available_tags = MTags.all();
    context['all_tags'] = available_tags;
    context['is_user'] = is_bt_user(request);
    context_instance=RequestContext(request);
    context_instance.autoescape=False;#POTENTIAL MARKL INJECT ATTACK
    return rtrg(template, context,context_instance);

def viewframedcontentV2(request, template='framed_link_content.html', extra_context=None):
    context = RequestContext(request);
    linkname = request.GET.get('l', '');

    #linkitem = get_object_or_404(Bbslinks,linkid);
    try:
        linkitem = Bbslinks.get_by_key_name( linkname );
    except Exception,e:
        try:
            linkitem = Bbslinks.get_by_id( linkname );
        except Exception,e:
            raise Http404;
        raise Http404;
    context['link'] = linkitem;
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
    context_instance=RequestContext(request);
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);


# OPERATION VIEWS THROUGH AJAX CALLS
def tagginglinks(request, template='tagging.json', extra_context=None):
    context = {};
    tag_name = request.POST['tagname'];
    linkid = request.POST['linkid'];
    valid_link = tag_name != None and linkid != None; # tag name in my list
    #or user == None or not users.is_current_user_admin()
    if( not valid_link  ):
        context['result'] = 0;
        return rtr(template, context,extra_context);
    try:
        linkitem = db.get(linkid);
    except:
        raise;
    
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
    
    try:
        linkitem = db.get(linkid);
    except:
        raise;
    
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
    
    try:
        linkitem = db.get(linkid);
    except:
        raise;
    
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

def toggle_ad_promotion(request, template='result.json', extra_context=None):
    status = OptionSet.getValue('adpromote',True);
    OptionSet.setValue('adpromote',not status );
    context = {};context['result'] = 1; 
    return rtr(template, context,extra_context);

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
    context_instance=RequestContext(request);
    context_instance.autoescape=False;
    return rtr(template, context,context_instance);



parser = BBSParser();
def gae_cron_job_parse( request , template='cron_result.html',extra_context=None):
    context=RequestContext(request);
    #now         = datetime.now()
    delta       = timedelta( minutes = -40 );
    criteria    = datetime.datetime.now() + delta;

    not_updated_list = get_object_list(ParseConfig, 'lastfresh < ', criteria, ' status =  ', STATUS_NORMAL ).order('lastfresh').order('failedparse');
    context['not_updated_count'] = len( not_updated_list );
    finished_name_list = [];
    duration = 0;
    
    for bbs_config in not_updated_list:
        #t1 = time.time();
        if( bbs_config.totalparse == 0 ): expected_parse_time = bbs_config.totalparsetime;
        else: expected_parse_time = bbs_config.totalparsetime / bbs_config.totalparse;
        if duration + expected_parse_time > parse_time_limit: break;
        parsetime = parser.parsebbs( bbs_config.toDict(), bbs_config );
        #t2 = time.time();
        finished_name_list.append( bbs_config.school.chinesename );
        duration += parsetime;
        if duration > parse_time_limit: break;
    context['updated_count']    = len( finished_name_list );
    context['finished_names']   = finished_name_list;
    context['duration']         = duration;
    context_instance=RequestContext(request);
    return render_to_response(template, context,context_instance);
    
    
@admin_user_only
def admin_db_op( request,  template='default.html', extra_context=None):
    context = RequestContext(request);
    if ( 'op' in request.GET and 'nm' in request.GET  ):
        op = request.GET['op'];
        bn = request.GET['nm'];
        
        if op == 'cron':
            try:
                sb = get_object(Schoolbbs,  'bbsname =',  bn );
                pc = get_object(ParseConfig, 'school = ', sb);
            except Exception,e:
                msg = 'error ocuured when cron school %s, %s'%(bn,e);
                context['msg'] = msg;
                return rtr( template, context, context_instance=extra_context);
            parser.parsebbs( pc.toDict(), pc );
            msg =  'Admin cron config %s from web request finished'%(bn);
            context['msg'] = msg;
            logging.info( msg );
    else: raise Http404;
    return rtr( template, context, context_instance=extra_context)

def gae_cron_job_sendblog( request , template='cron_mblog_result.html',extra_context=None):
    context=RequestContext(request);
    #now         = datetime.now()
    delta       = timedelta( hours = -4 );
    criteria    = datetime.datetime.now() + delta;

    hourlylinks = get_object_list( Bbslinks, 'createtime > ', criteria ).order('-createtime').order('-visitcount');
    recommend_count = 0;
    sina_list = [];n163_list = [];twitter_list=[];
    
    bhandle = Microblog();
    for links in hourlylinks:
        if( not bhandle.skip_sina and not links.contain_tag( SINA_MBLOG ) ): 
            sina_list.append( links );
            links.tags.append( SINA_MBLOG );
            recommend_count += 1;
        if( not bhandle.skip_n163 and not links.contain_tag( N163_MBLOG ) ): 
            n163_list.append( links );
            links.tags.append( N163_MBLOG );
            recommend_count += 1;
        if( not bhandle.skip_twitter and not links.contain_tag( TWITTER_MBLOG ) ): 
            twitter_list.append( links );
            links.tags.append( TWITTER_MBLOG );
            recommend_count += 1;
        links.put();
        if( recommend_count > bhandle.quota ):break;
    
    
    for links in sina_list:
        bhandle.post_sina_msg( links.get_mblog_str() );
    for links in n163_list:
        bhandle.post_n163_msg( links.get_mblog_str() );
    for links in twitter_list:
        bhandle.post_twitter_msg( links.get_mblog_item() );
  
    context['sina_count']    = len( sina_list );
    context['n163_count']    = len( n163_list );
    context['twitter_count']    = len( twitter_list );
    context_instance=RequestContext(request);
    return render_to_response(template, context,context_instance);


@admin_user_only 
def gae_setup_initial_data( request , template='cron_result.html',extra_context=None):

    for bc in bbs_setting_list :
            item = get_object(Schoolbbs,  'schoolname =',  bc['schoolname'] );
            if not item :
                
                school = db_create( Schoolbbs, lastfresh = datetime.datetime.now(), **bc );
                if( bc['bbsname'] != 'recommend' ):
                    config = db_create( ParseConfig,  school = school, **bc );
                
    return HttpResponse('All School data setup successfully');
	
##########################################################################################################
#Util method defined to help with pagination links
def paginate( query, page_number , context, pagesize = PAGE_SIZE, orderby="-updatetime" ):
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
    
    
    result_link_page = query.order( orderby ).fetch( (page_number+1)*pagesize, page_number*pagesize );
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
##########################################################################################################	
def bg_addstaic_data(request, template='tagging.json', extra_context=None):
	context = {};
	if request.method == 'POST' and 'abstract' in request.POST:
		static = db_create( BGFriendStatics, abstract = request.POST['abstract'] ,
			score = int( request.POST['score'] ),
			type = request.POST['type'], ip = request.META['REMOTE_ADDR']);
		context['result'] = True;
		context['id'] = unicode( static.key() );
	else:
		context['result'] = False;
	return HttpResponse( simplejson.dumps(context,ensure_ascii = False) ); 
	
def bg_addstaic_rank(request, template='tagging.json', extra_context=None):
	context = {};
	if request.method == 'POST' and 'id' in request.POST:
		try:
		    abstract_item = db.get(  request.POST['id']  );
		except Exception,e:
			context['result'] = False;
			context['msg']= str(e);
			return HttpResponse( simplejson.dumps(context,ensure_ascii = False) );
			
		static = db_create( BGFriendRank, abstract = abstract_item ,
			 fillee = request.POST['fillee'], bgfriend=request.POST['bgfriend'] );
		context['result'] = True;
		
	else:
		context['result'] = False;
	return HttpResponse( simplejson.dumps(context,ensure_ascii = False) ); 

def static_result(request, template='bgresult.html', extra_context=None):
	context=RequestContext(request);
	if 'op' in request.GET :
		if request.GET['op']=='rank':
			context['list'] = get_object_list( BGFriendRank );
			context['op'] 	= True;
		elif request.GET['op']=='static':
			context['list'] = get_object_list( BGFriendStatics );
			context['op'] 	= False;
	else:
		context['list'] = get_object_list( BGFriendStatics );
		context['op'] 	= False;

	return render_to_response(template, context,extra_context);
	

	
    