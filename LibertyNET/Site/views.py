from django.core.context_processors import request
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from Common.helpermethods import create_address_helper, form_generator, create_contact_helper, \
    validation_helper, dict_generator, update_address_helper, update_contact_helper
from Client.models import Client
from Site.models import Site
from Common.models import Address, CallList

#region ClientSite


def editclientsite(request, pk):
    template_name = 'client/editclientsite.html'
    site = Site.objects.get(site_id=pk)
    form_list = form_generator(1)
    if request.method == 'POST':
        validation = validation_helper(form_list)
        if validation:
            return HttpResponseRedirect(reverse('Client:index'))
        else:
            return HttpResponseRedirect(reverse('Client:editclientsite'))
    else:

        return render(request, template_name, dict_generator(form_list))


class SiteDetailView(DetailView):
    model = Site
    site_id = 'pk'
    context_object_name = 'site_detail'
    template_name = 'client/sitedetails.html'

    def get_context_data(self, **kwargs):
        context = super(SiteDetailView, self).get_context_data(**kwargs)
        site = self.get_object()
        client = Client.objects.get(pk=site.site_client_id)
        context['client_detail'] = Client.objects.get(pk=client.client_id)
        context['address_detail'] = Address.objects.get(pk=client.client_address_id)
        context['calllist_detail'] = site.site_call_list.all()

        return context

#endregion
