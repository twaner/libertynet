from django import template
from Common.helpermethods import show_login
from django.shortcuts import redirect, HttpResponseRedirect
from django.core.context_processors import request
from django.core.urlresolvers import reverse


register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='addstyle')
def addstyle(field, mystyle):
    return field(attrs={"style": mystyle})

@register.simple_tag
def user_name(user):
    return '%s %s' % (user.first_name, user.last_name)


#register.inclusion_tag("/Common/login.html")(show_login)

@register.inclusion_tag("common/login.html")
def show_login(request):
    print('SHOW_LOGIN REQUEST %s' % request)
    print('show_login: /common/login/?next=%s' % request.path)
    return redirect('/common/login/?next=%s' % request.path)
    #return HttpResponseRedirect(reverse('Common:login/?next=%s' % request.path))



    # "middle_initial"
    # "last_name"
    # "client_number"
    # "business_name"
    # "is_business"
    # "client_date"
