# Introduction #
this is actually fucking stupid plugin which needs totally rewrites and understanding

NOTE:
if your xn app is iframe, then many redirects in the code need to be manually modified
if your xn app is iframe, then some functions need to be rwritten to avoid the stupid XNML

how pyxn works:
first through register a middleware,
//( not correct )then during each request, you need to using @require\_add to inject stupid keys into request
during each request, an Xiaonei object is constructed. ...debugging......
it will inject dynamic method into this object, like:
DEBUG    2010-10-17 14:29:54,773 init.py:398] Adding method?:feed , FeedProxy(self, 'xiaonei.feed')
DEBUG    2010-10-17 14:29:54,773 init.py:398] Adding method?:profile , ProfileProxy(self, 'xiaonei.profile')
DEBUG    2010-10-17 14:29:54,776 init.py:398] Adding method?:users , UsersProxy(self, 'xiaonei.users')
DEBUG    2010-10-17 14:29:54,778 init.py:398] Adding method?:admin , AdminProxy(self, 'xiaonei.admin')
DEBUG    2010-10-17 14:29:54,779 init.py:398] Adding method?:pay , PayProxy(self, 'xiaonei.pay')
DEBUG    2010-10-17 14:29:54,782 init.py:398] Adding method?:invitations , InvitationsProxy(self, 'xiaonei.invitations')
DEBUG    2010-10-17 14:29:54,783 init.py:398] Adding method?:notifications , NotificationsProxy(self, 'xiaonei.notifications')
DEBUG    2010-10-17 14:29:54,785 init.py:398] Adding method?:friends , FriendsProxy(self, 'xiaonei.friends')
I am not going to use any of these, so neglect these.

and then self.auth = AuthProxy(self, 'xiaonei.auth')
//(not) SEEMINGLY ALL THESE PROXIES ARE EXECed

seemingly mis-understanding here

servers can not communicate with XN directly using API
Try using ordinary spider. FK that.



# Details #

Add your content here.  Format your content with:
  * Text in **bold** or _italic_
  * Headings, paragraphs, and lists
  * Automatic links to other wiki pages