# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from django.template import RequestContext

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _


#from gaegene.pagination.models import *;
#from gaegene.pagination.views import object_list
from django.core.paginator import Paginator as ObjectPaginator, InvalidPage, EmptyPage
from google.appengine.ext import db
from ragendja.dbutils import *;
from django.shortcuts import render_to_response
from content.models import *;



def viewbylinks( request, pagenumber=1,
                    template_name='bbs-template.html',
                    extra_context=None):
             
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request);
    
    #object_query = Bbslinks.all()
    object_query = get_object_list(Bbslinks);
    #order_property = '-visitcount'
    #template_name = 'pagination/test.html'
    #paginator = ObjectPaginator(object_query,10)
    """
    try:
        object_list = paginator.page(pagenumber)
    except (EmptyPage, InvalidPage):
        object_list = paginator.page(paginator.num_pages)

    prefetch_references( object_list.object_list, 'school')
    
    """
    """
    for link in object_list.object_list:
        link.pschool = link.school;
        """
    object_list = object_query;
    schoolkeys  = [Bbslinks.school.get_value_for_datastore(Link) for Link in object_list]
    schools     = db.get(schoolkeys)
    for link,school in zip(object_list,schools):
        link.pschool = school;

    #link1 = object_list.object_list[0];
    #s = link.school
    #name = link.school_name；
    #print s.bbsname;
    #object_list.debug
    return render_to_response( template_name,
                               { 'object_list': object_list,},
                               context_instance=context)
    
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
                'name':         unicode(school.schoolname),
                'chinesename':  unicode(school.chinesename),
                'itemlist':     toptenlist,
    }
    return bbsinfo;
    
def viewbyschool(request, template='content_by_school.html',
                    extra_context=None):
    
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request);
    bbsnamelist = [];
    highschoollist = Schoolbbs.all();
    count = highschoollist.count();
    highschoollist.order('rank');
    for item in highschoollist[0:20]:
        bbsnamelist.append(item.bbsname);
    if 'selectedtop1' in request.COOKIES and request.COOKIES['selectedtop1']:
        favbbs = request.COOKIES['selectedtop1'];
        try:
            i = bbsnamelist.index(favbbs)
            bbsnamelist.remove(favbbs)
            bbsnamelist.insert(0, favbbs);
        except ValueError:
            bbsnamelist.insert(0, favbbs);
            bbsnamelist.pop();
            
    bbslist = [];
    #print bbsnamelist;
    for name in  bbsnamelist:
        bbslist.append(getBbsListBySchool(name));
    """
    "
    if  count >= 20:
        cardlist = bbslist[0:20];
    else:
         cardlist = bbslist;
    if  ('card' in request.GET) : 
        return render_to_response('list_card.html', {'context':cardlist});
    """
    
    bbstoplist = bbslist[0:20];
    #recolist = MostTopTenItem.all();
    context['col1'] = bbstoplist[0:9];
    context['col2'] = bbstoplist[10:20];
    return render_to_response(template, context);
    


    