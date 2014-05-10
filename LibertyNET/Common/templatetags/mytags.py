from django import template
register = template.Library()

@register.filter(name='addcss')
def addcss(field, css):
    return field.as_widget(attrs={"class": css})

@register.filter(name='addstyle')
def addstyle(field, mystyle):
    return field(attrs={"style": mystyle})


    # "middle_initial"
    # "last_name"
    # "client_number"
    # "business_name"
    # "is_business"
    # "client_date"
