from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from models import Client, Sales_Prospect
from helpermethods import create_client_helper, create_sales_prospect_helper
from forms import ClientForm, SalesProspectForm
from Common.forms import AddressForm, ContactForm
from Common.helpermethods import create_address_helper, form_generator, create_contact_helper,\
    validation_helper, dict_generator

#region GenericViews


class ClientListView(ListView):
    model = Client
    context_object_name = 'all_client_list'
    template_name = 'client/index.html'


class ClientDetailList(ListView):
    template_name = 'client/detail.html'

    def get_queryset(self):
        self.client = get_object_or_404(Client, name=self.args[0])
        return Client.objects.filter(client=self.client)


class SalesProspectListView(ListView):
    model = Sales_Prospect
    context_object_name = 'all_sales_prospect_list'
    template_name = 'client/salesprospectindex.html'

#endregion

#region AddClientView


def addclient(request):
    form_list = form_generator(4)
    if request.method == 'POST':
        form_list[0] = ClientForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address = create_address_helper(request)
            contact = create_contact_helper(request)
            client = create_client_helper(request, address, contact)
            #return HttpResponseRedirect('/client/index/')
            return HttpResponseRedirect(reverse('Client:index'))
    else:
        form_list[0] = ClientForm()
        form_list[1] = AddressForm()
        form_list[2] = ContactForm()
    form_dict = dict_generator(form_list)

    return render(request, 'client/addclient.html', form_dict)

#endregion

#region SalesProspect View


class SalesProspectView(View):
    form_class = Sales_Prospect
    template_name = 'client/addsalessprospect.html'
    form_list = form_generator(3)

    def post(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = SalesProspectForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address = create_address_helper(request)
            contact = create_contact_helper(request)
            sales_prospect = create_sales_prospect_helper(request, address=address, contact=contact)
            return HttpResponseRedirect(reverse('Client:salesprospectindex'))


    def get(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = SalesProspectForm()
        form_list[1] = AddressForm()
        form_list[2] = ContactForm()
        form_dict = dict_generator(form_list)
        return render(request, self.template_name, form_dict)




#endregion

#region Billing Views


def addbilling(request, client_id):
    pass
    #TODO Create view to add billing information

#endregion
