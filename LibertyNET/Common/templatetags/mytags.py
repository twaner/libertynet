from django import template
from django.shortcuts import redirect, HttpResponseRedirect
from django.core.context_processors import request
from django.core.urlresolvers import reverse
from Common.helpermethods import show_login


register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    """
    Allows Css Class to be added to a field.
    @param field: field that CSS will be applied to.
    @param css: CSS Class
    @return: field with CSS class.
    """
    return field.as_widget(attrs={"class": css})

@register.filter(name='addstyle')
def addstyle(field, mystyle):
    return field(attrs={"style": mystyle})

@register.simple_tag
def user_name(user):
    return '%s %s' % (user.first_name, user.last_name)

#register.inclusion_tag("/Common/login.html")(show_login)

#region Number Decorators

@register.filter(name='to_percent')
def percentify(val):
    """
    Takes a value and returns it as a Percentage - .25 to 25%.
    @param val: Value to be updated.
    @return: Number in percent format
    """
    if val >= 1:
        q = format(val, "%")
    elif val < 1:
        q = "{0:.0f}".format(float(val) * 100)
    return q


@register.filter(name='negative_decorator')
def negativify(val):
    if str(val)[0] == '-':
        tmp = str(val)[1:]
        return '({0})'.format(tmp)
    else:
        return val



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
