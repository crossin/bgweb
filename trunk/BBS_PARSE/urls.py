# Copyright 2008 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from django.conf.urls.defaults import *
from feeds import RssSiteContentFeed, AtomSiteContentFeed  


feeds = {  
    'content': RssSiteContentFeed,
    'content': AtomSiteContentFeed,
}  


urlpatterns = patterns(
    '',
    (r'^$', 'views.getbbs'),
    (r'^xn/', 'views.getbbs4xn'),
    (r'^namelist/', 'views.get_bbsnamelist'),
    (r'^listall$', 'views.getfullbbslist'),
    (r'^recommended$', 'views.getRecommended'),
    (r'^list$', 'views.getbbs'),
#    (r'^topmost/','views.getMostTop10'),
    (r'^fresh1/', 'views.getFreshBBS1'),
    (r'^fresh2/', 'views.getFreshBBS2'),
    (r'^fresh3/', 'views.getFreshBBS3'),
    (r'^rss/', 'feeds.rss201'),
    (r'^rss/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',{'feed_dict': feeds}),
    (r'^atom/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',{'feed_dict': feeds}),
#    (r'^service/bbs/', 'bbsservice.bbsGateway'),
)
