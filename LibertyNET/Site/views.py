from django.core.context_processors import request
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from Common.helpermethods import create_address_helper, form_generator, \
    validation_helper, dict_generator, update_address_helper, update_contact_helper, \
    create_contact_client_calllog_helper, create_call_list_helper, create_call_list_helper_not_site
from Client.models import Client
from Site.models import Site
from Site.forms import SiteForm
from Site.helper_methods import create_site_helper, update_site_helper
from Common.models import Address, CallList, Contact
from Common.forms import AddressForm, CallListForm, CallListContactForm

#region ClientSite


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
        context['calllist_detail'] = site.site_call_list.all().order_by('cl_order')
        context['calllist_active'] = site.site_call_list.filter(cl_is_enabled=True)

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
    form_list[3] = CallListContactForm(request.POST)
    site_dict = {
        'site_client': client.client_id
    }
    call_dict = {
        'first_name': client.first_name,
        'middle_initial': client.middle_initial,
        'last_name': client.last_name
    }
    if request.method == 'POST':
        if validation_helper(form_list):
            address = create_address_helper(form_list[1])
            contact = create_contact_client_calllog_helper(form_list[3])
            calllist = create_call_list_helper_not_site(form_list[2], contact)
            site = create_site_helper(form_list[0], client, address, calllist)
            return HttpResponseRedirect(reverse('Client:sitedetails',
                                        kwargs={'pk': site.site_id}))
        else:
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = SiteForm(site_dict)
        form_list[1] = AddressForm()
        form_list[2] = CallListForm(call_dict)
        form_list[3] = CallListContactForm()

        return render(request, template_name, dict_generator(form_list))


def editclientsite(request, pk):
    """
    View to edit Site Details
    @param request: request.
    @param pk: Site PK.
    @return: HttpResponse.
    """
    template_name = 'client/editclientsite.html'
    form_list = form_generator(2)
    site = Site.objects.get(pk=pk)
    address = Address.objects.get(pk=site.site_address.id)
    call_list = CallList.objects.filter(site=site.site_id)
    # Dictionaries to bind forms
    site_dict = {
        'site_name': site.site_name, 'site_client': site.site_client,
    }
    address_dict = {
        'street': address.street, 'unit': address.unit, 'city': address.city,
        'state': address.state, 'zip_code': address.zip_code
    }

    # POST
    if request.method == 'POST':
        form_list[0] = SiteForm(request.POST)
        form_list[1] = AddressForm(request.POST)

        if validation_helper(form_list):
            a = update_address_helper(request, address)
            site = update_site_helper(form_list[0], a, site)
            return HttpResponseRedirect(reverse('Client:sitedetails',
                                        kwargs={'pk': site.site_id}))
        else:
            return render(request, template_name, dict_generator(form_list))

    else:
        form_list[0] = SiteForm(site_dict)
        form_list[1] = AddressForm(address_dict)
        fd = dict_generator(form_list)
        fd['client'] = site.site_client
        fd['site'] = site
        return render(request, template_name, fd)

#endregion
