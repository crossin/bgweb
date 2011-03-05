# -*- coding: utf-8 -*-
from django import forms;
from django.utils.translation import ugettext_lazy as _, ugettext as __
from models import *;
import datetime;


class AccountForm(forms.ModelForm):
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(maxlength=75)),  label=_(u'Email:'))
    class Meta:
        model = UserAccount;
    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        q = UserAccount.all().filter( 'email =', self.cleaned_data['email'] );
        if( q.count() != 0 ):
            raise forms.ValidationError(__(u'This Email is already taken. Please choose another.'))
        return self.cleaned_data['email']
        
    def save(self):
        account = UserAccount( email = self.cleaned_data['email']);
        self.instance = account;
        return super(AccountForm, self).save();
    
    def getinfo(self):
        return self.errors['email'];

        
class AnnouncementForm(forms.ModelForm):
    ann = forms.CharField(widget=forms.widgets.Textarea(),  label=_(u'content:'))
    class Meta:
        model = Announcement;
        
    def save(self):
        q = Announcement.all();
        if( q.count() == 0 ):
            announce = Announcement( content = self.cleaned_data['ann'] );
            self.instance = announce;
        else:
            announce = q.fetch(1)[0];
            announce.content = self.cleaned_data['ann'];
            self.instance = announce;
        return self.instance.put();#different from saving a new object here
    def getinfo(self):
        return self.errors['ann'];
    
class MTagsForm(forms.ModelForm):
    name = forms.CharField(required=True, label='Name')
    class Meta:
        model = MTags;
    def clean_name(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        q = MTags.all().filter( 'name =', self.cleaned_data['name'] );
        if( q.count() != 0 ):
            raise forms.ValidationError(__(u'This name is already taken. Please choose another.'))
        return self.cleaned_data['name'];
        
    def save(self):
        tag = MTags( name = self.cleaned_data['name'] );
        self.instance = tag;
        return super(MTagsForm, self).save();
    
    def getinfo(self):
        return self.errors['name'];
    
    
    
class LinkForm(forms.Form):
    author      = forms.CharField(widget=forms.TextInput(attrs=dict(maxlength=10)) , required=True, label=u'Author:')
    title       = forms.CharField(widget=forms.TextInput(attrs=dict(maxlength=200)), required=True, label=u'Title:')
    keyword     = forms.CharField(widget=forms.TextInput(attrs=dict(maxlength=10)) , required=True, label=u'Keyword:')
    link        = forms.CharField(widget=forms.TextInput(attrs=dict(maxlength=500)), required=True, label=u'link:')
    class Meta:
        model = Bbslinks;
    def clean_link(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        """
        q = Bbslinks.all().filter( 'titlelink =', self.cleaned_data['link'] );
        if( q.count() != 0 ):
            raise forms.ValidationError(__(u'This link is already taken. Please choose another.'));
        return self.cleaned_data['link'];
        
    def save(self):
        qs = Schoolbbs.all().filter( 'bbsname =', 'recommend' ).fetch(1);
        l  = Bbslinks( author = self.cleaned_data['author'], title = self.cleaned_data['title'], 
                titlelink = self.cleaned_data['link'],  board=self.cleaned_data['keyword'], source='recommend', tags=[u'推荐'],
              createtime = datetime.datetime.now(),
              updatetime = datetime.datetime.now(), school=qs[0] );
        l.put();
        LinkTags( name=u"推荐", link = l ).put();
        return l;
    
    def getinfo(self):
        return u'请检查您的输入是否有误  或者 这篇帖子已经是一篇老物了'; 
          