# -*- coding: utf-8 -*-
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _

from models import *;
#from gaegene.pagination.models import *;
#from gaegene.pagination.views import object_list
from django.core.paginator import Paginator as ObjectPaginator, InvalidPage, EmptyPage
from google.appengine.ext import db
from ragendja.dbutils import *;




def list(request, 
            pagenumber=1,
            template_name='content/index-content-list.htm',
            extra_context=None):
             
    if extra_context is None:
        extra_context = {}
    context = RequestContext(request);
    
    #object_query = Bbslinks.all()
    object_query = get_object_list(Bbslinks);
    #order_property = '-visitcount'
    #template_name = 'pagination/test.html'
    paginator = ObjectPaginator(object_query,10)
    try:
        object_list = paginator.page(pagenumber)
    except (EmptyPage, InvalidPage):
        object_list = paginator.page(paginator.num_pages)

    prefetch_references( object_list.object_list, 'school')
    
    """
    for link in object_list.object_list:
        link.pschool = link.school;
        """
    schoolkeys  = [Bbslinks.school.get_value_for_datastore(Link) for Link in object_list.object_list]
    schools     = db.get(schoolkeys)
    for link,school in zip(object_list.object_list,schools):
        link.pschool = school;

    link1 = object_list.object_list[0];
    #s = link.school
    #name = link.school_name；
    #print s.bbsname;
    #object_list.debug
    return render_to_response( template_name,
                               { 'object_list': object_list,
                                
                                  },
                              context_instance=context)



    