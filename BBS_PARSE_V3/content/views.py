# -*- coding: utf-8 -*-
from datetime import *;
import time;
import random;
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import *
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.shortcuts import render_to_response as rtr;

from ragendja.dbutils import *;
from ragendja.mrender import render_to_response as rtrg;

from pageharvest.settings import *;
from pageharvest.bbs_parser import *;
from settings import *;

from models import *;
from decorators import *;
from form import *;

from adsys.decorators import random_record_xn_access;

    
    
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

    
@admin_user_only  
def addannouncement(request, template='result.json', extra_context=None):
    return ajax_operation( AnnouncementForm, request, template, extra_context );




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
