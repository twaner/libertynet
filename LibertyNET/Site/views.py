from django.core.context_processors import request
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from Common.helpermethods import create_address_helper, form_generator, create_contact_helper, \
    validation_helper, dict_generator, update_address_helper, update_contact_helper, \
    create_call_list_helper
from Client.models import Client
from Site.models import Site
from Site.forms import SiteForm
from Site.helper_methods import create_site_helper
from Common.models import Address, CallList
from Common.forms import AddressForm, CallListForm

#region ClientSite


def editclientsite(request, pk):
    """
    Edits a Client's Site.
    @param request: request.
    @param pk: primary key.
    @return: html redirect.
    """
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
        context['calllist_detail'] = site.site_call_list.all().order_by('-cl_order')

        return context


def addclientsite(request, pk):
    """
    Creates a Site for a Client.
    @param request: request.
    @param pk: Client pk.
    @return: Http response.
    """
    template_name = 'client/addclientsite.html'
    form_list = form_generator(4)
    client = Client.objects.get(pk=pk)
    form_list[0] = SiteForm(request.POST)
    form_list[1] = AddressForm(request.POST)
    form_list[2] = CallListForm(request.POST)
    site_dict = {
        'site_client': client.client_id
    }

    if request.method == 'POST':
        if validation_helper(form_list):
            address = create_address_helper(form_list[1])
            calllist = create_call_list_helper(form_list[2])
            site = create_site_helper(form_list[0], client, address, calllist)
            return HttpResponseRedirect('Client:sitedetails',
                                        kwargs={'pk': site.site_id})
        else:
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = SiteForm(site_dict)
        form_list[1] = AddressForm()
        form_list[2] = CallListForm()
        return render(request, template_name, dict_generator(form_list))


#endregion
