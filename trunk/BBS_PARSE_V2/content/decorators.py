# -*- coding: utf-8 -*-
from functools import wraps;
from ragendja.auth.decorators import *;
from google.appengine.api import users;
from content.models import UserAccount;
from django.template import RequestContext

def bt_user_only(view):
    """
    Decorator that requires user.is_staff. Otherwise renders no_access.html.
    """
    @google_login_required
    def wrapped(request, *args, **kwargs):
        uea = request.META['USER_EMAIL'];
        q = UserAccount.all().filter('email =',uea );
        if q.count() > 0 :
            return view(request, *args, **kwargs)
        context = RequestContext(request);
        return render_to_response( 'access_limited.html', context,context)
    return wraps(view)(wrapped)


def admin_user_only(view):
    """
    Decorator that requires user.is_staff. Otherwise renders no_access.html.
    """
    @google_login_required
    def wrapped(request, *args, **kwargs):
        if users.is_current_user_admin():
            return view(request, *args, **kwargs)
        context = RequestContext(request);
        return render_to_response( 'access_limited.html', context,context)
    return wraps(view)(wrapped)

def is_bt_user( request ):
    email = request.META['USER_EMAIL'];
    if( email == None ): return False;
    q = UserAccount.all().filter('email =',email );
    return q.count() > 0;