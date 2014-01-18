from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from models import Client, Sales_Prospect
from forms import ClientForm
from helpermethods import create_employee_helper, create_employee_worker
from Common.forms import AddressForm, ContactForm
from Common.helpermethods import create_address_helper, create_employee_contact_helper, form_generator, \
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
