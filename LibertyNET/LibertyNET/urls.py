from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
dajaxice_autodiscover()
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'employee/', include('Employee.urls', namespace="Employee")),
                       url(r'client/', include('Client.urls', namespace="Client")),
                       url(r'equipment/', include('Equipment.urls', namespace="Equipment")),
                       url(r'site/', include('Site.urls', namespace="Site")),
                       url(r'vendor/', include('Vendor.urls', namespace="Vendor")),
                       url(r'work/', include('Work.urls', namespace="Work")),
                       url(r'common/', include('Common.urls', namespace="Common")),
                       url(r'^admin/', include(admin.site.urls)),
                       url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)

urlpatterns += staticfiles_urlpatterns()

