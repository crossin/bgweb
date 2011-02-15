from django.conf.urls.defaults import *;
from django.views.generic.simple import direct_to_template;
from django.contrib.auth import views as auth_views;

from content.views import *;

urlpatterns = patterns('',
    url(r'^list/(?P<pagenumber>\d+)/$', viewbylinks, 
        {'template': 'content_by_list.html'},       name='content_list'),
    url(r'^list/$', viewbylinks, 
        {'template': 'content_by_list.html'},       name='content_list_home'),
    url(r'^home/$', viewbyschool, 
        {'template': 'content_by_school.html'},     name='content_home'),
    url(r'^detail/$',viewframedcontent,
        {'template':'framed_link_content.html'},    name='content_framed_detail'),
    url(r'^account/$',viewaccount,
        {'template':'account_interface.html'},      name='viewaccount'),
    url(r'^search/(?P<tagname>\w+)/(?P<pagenumber>\d+)/$', searchlinksbytag, 
        {'template': 'search_interface.html'},      name='searchlistbytag'),
    url(r'^search/$', searchlinksbypost, 
        {'template': 'search_interface.html'},      name='postsearchlist'),
    url(r'^xn/$', viewxnhome, 
        {'template': 'xn_interface.html'},          name='xncontent_home'),
    url(r'^xn/(?P<pagenumber>\d+)/$', viewxnhome, 
        {'template': 'xn_interface.html'},          name='xncontent_list'),
    #shorten the stupid long url.
    url(r'^go$',viewframedcontentV2,
        {'template':'framed_link_content.html'},    name='content_framed_detailV2'),
    url(r'^status/$',view_parsing_status,
        {'template':'school_status_list.html'},    name='view_parsing_status'),
        
        
    url(r'^operation/tagging/$', tagginglinks, 
        {'template': 'tagging.json'} ,      name='tagginglinks'),
    url(r'^operation/rating/$', ratinglinks, 
        {'template': 'result.json'} ,       name='ratinglinks'),
    url(r'^operation/comment/$', commentlink, 
        {'template': 'result.json'} ,       name='commentlink'),
    url(r'^operation/addtag/$', addtag, 
        {'template': 'result.json'} ,       name='addtag'),
    url(r'^operation/getcomment/$', getcomments, 
        {'template': 'comment.html'} ,      name='getcomments'),
        
    url(r'^operation/addlink/$', addlink, 
        {'template': 'result.json'} ,       name='addlink'),
    url(r'^operation/addannouncement/$', addannouncement, 
        {'template': 'result.json'} ,       name='addannouncement'),
    url(r'^operation/addaccount/$', addaccount, 
        {'template': 'result.json'} ,       name='addaccount'), 
    url(r'^operation/toggle_ad_promotion/$', toggle_ad_promotion, 
        {'template': 'result.json'} ,       name='toggle_ad_promotion'), 
        
        
    url(r'^management/home/$', manangement, 
        {'template': 'admin_interface.html'} ,      name='mgmthome'),
    url(r'^management$', admin_db_op, 
        {'template': 'default.html'} ,      name='adminop'),
        
    url(r'^management/cron/$', gae_cron_job_parse, 
        {'template': 'cron_result.html'} ,      name='mgmtcron'),
    url(r'^management/mblog/$', gae_cron_job_sendblog, 
        {'template': 'cron_mblog_result.html'} ,      name='mgmtcron_mblog'),
    url(r'^management/setup/$', gae_setup_initial_data, 
        {'template': 'cron_result.html'} ,      name='mgmtstup'),
		
	url(r'^bg/addstatic/$', bg_addstaic_data, 
        {'template': 'cron_result.html'} ,      name='bg_addstaic_data'),
	url(r'^bg/addrank/$', bg_addstaic_rank, 
        {'template': 'cron_result.html'} ,      name='bg_addstaic_rank'),
	url(r'^bg/view/$', static_result, 
        {'template': 'bgresult.html'} ,      name='bg_view'),
    
)
