from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from models import Client, Sales_Prospect
from helpermethods import create_client_helper
from forms import ClientForm
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

#endregion

#region AddClientView


class addclient(request):
    form_list = form_generator(4)
    if request.method == 'POST':
        form_list[0] = ClientForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address = create_address_helper(request)
            contact = create_contact_helper(request)
            client = create_client_helper



#endregion
