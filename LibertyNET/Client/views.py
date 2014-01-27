from django.core.context_processors import request
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from models import Client, Sales_Prospect
from helpermethods import create_client_helper, create_sales_prospect_helper, update_client_helper, \
    update_sales_prospect_helper
from forms import ClientForm, SalesProspectForm
from Common.forms import AddressForm, ContactForm
from Common.models import Address, Contact, Billing
from Common.helpermethods import create_address_helper, form_generator, create_contact_helper,\
    validation_helper, dict_generator, update_address_helper, update_contact_helper

#region GenericViews


class ClientListView(ListView):
    model = Client
    context_object_name = 'all_client_list'
    template_name = 'client/index.html'


class ClientDetailList(ListView):
    model = Client
    template_name = 'client/detail.html'
    context_object_name = 'client_detail'

    def get_queryset(self):
        self.client = get_object_or_404(Client, client_id=self.args[0])
        return Client.objects.filter(pk=self.client_id)


class ClientDetailView(DetailView):
    model = Client
    client_id = 'pk'
    context_object_name = 'client_detail'
    template_name = 'client/details.html'

    def get_context_data(self, **kwargs):
        context = super(ClientDetailView, self).get_context_data(**kwargs)
        client = self.get_object()
        context['address_detail'] = Address.objects.get(pk=client.client_address_id)
        context['contact_detail'] = Contact.objects.get(pk=client.client_contact_id)

        return context


class SalesProspectListView(ListView):
    model = Sales_Prospect
    context_object_name = 'all_sales_prospect_list'
    template_name = 'client/salesprospectindex.html'


class SalesProspectDetailView(View):
    model = Sales_Prospect
    sales_prospect_id = 'pk'
    template_name = 'client/salesprospectdetails.html'
    context_object_name = 'sales_prospect_detail'

    def get_context_data(self, **kwargs):
        context = super(SalesProspectDetailView, self).get_context_data(**kwargs)
        sales = self.get_object()
        try:
            context['address_detail'] = Address.objects.get(pk=sales.sp_address_id)
        except Address.DoesNotExist:
            pass
        try:
            context['contact_detail'] = Contact.objects.get(pk=sales.sp_contact_id)
        except Contact.DoesNotExist:
            pass
        return context


def salesprospectdetails(request, sales_prospect_id):
    sales_prospect_detail = Sales_Prospect.objects.get(pk=sales_prospect_id)
    try:
        address_detail = Address.objects.get(pk=sales_prospect_detail.sp_address_id)
    except Address.DoesNotExist:
        address_detail = None
    contact_detail = Contact.objects.get(pk=sales_prospect_detail.sp_contact_id)
    context = {
        'sales_prospect_detail': sales_prospect_detail, 'address_detail': address_detail,
        'contact_detail': contact_detail
    }
    return render(request, 'client/salesprospectdetails.html', context)

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


def editsalesprospect(request, pk):
    form_list = form_generator(3)
    sales = Sales_Prospect.objects.get(pk=pk)
    contact = Contact.objects.get(pk=sales.sp_contact_id)
    try:
        address = Address.objects.get(pk=sales.sp_address_id)
    except ObjectDoesNotExist:
        address = None
    # Dictionaries to bind to form
    if address is not None:
        address_dict = {
            'street': address.street, 'unit': address.unit, 'city': address.city,
            'state': address.state, 'zip_code': address.zip_code
        }
    else:
        address_dict = {
            'street': '', 'unit': '', 'city': '',
            'state': '', 'zip_code': ''
        }
    contact_dict = {
        'phone': contact.phone, 'phone_extension': contact.phone_extension,
        'cell': contact.cell, 'email': contact.email, 'website': contact.website,
        'work_email': contact.work_email, 'office_phone': contact.office_phone,
        'office_phone_extension': contact.office_phone_extension
    }
    sales_dict = {
        'first_name': sales.first_name, 'middle_initial': sales.middle_initial,
        'last_name': sales.last_name, 'sp_business_name': sales.sp_business_name,
        'is_business': sales.is_business, 'sp_liberty_contact': sales.sp_liberty_contact_id,
        'sales_type': sales.sales_type, 'sales_probability': sales.sales_probability,
        'initial_contact_date': sales.initial_contact_date, 'comments': sales.comments
    }
    if request.method == 'POST':
        form_list[0] = SalesProspectForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address_up = update_address_helper(request, address)
            contact_up = update_contact_helper(request, contact)
            sales_up = update_sales_prospect_helper(request, address_up, contact_up)

            return HttpResponseRedirect(reverse('Client:salesprospectindex'))
    else:
        form_list[0] = SalesProspectForm(sales_dict)
        form_list[1] = AddressForm(address_dict)
        form_list[2] = ContactForm(contact_dict)
    form_dict = dict_generator(form_list)
    return render(request, 'client/editsalesprospect.html', form_dict)

#endregion

#region ClientViews


class ClientView(View):
    form_class = Client
    template_name = 'client/addclient.html'
    form_list = form_generator(3)

    def post(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = ClientForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address = create_address_helper(request)
            contact = create_contact_helper(request)
            client = create_client_helper(request, address, contact)
            return HttpResponseRedirect(reverse('Client:index'))

    def get(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = ClientForm()
        form_list[1] = AddressForm()
        form_list[2] = ContactForm()
        form_dict = dict_generator(form_list)
        return render(request, 'client/addclient.html', form_dict)


def editclient(request, client_id):
    form_list = form_generator(3)
    client = Client.objects.get(pk=client_id)
    address = Address.objects.get(pk=client.client_address_id)
    contact = Contact.objects.get(pk=client.client_contact_id)
    # Create dictionaries to bind to forms
    address_dict = {
        'street': address.street, 'unit': address.unit, 'city': address.city,
        'state': address.state, 'zip_code': address.zip_code
    }
    contact_dict = {
        'phone': contact.phone, 'phone_extension': contact.phone_extension,
        'cell': contact.cell, 'email': contact.email, 'website': contact.website,
        'work_email': contact.work_email, 'office_phone': contact.office_phone,
        'office_phone_extension': contact.office_phone_extension
    }
    client_dict = {
        'first_name': client.first_name, 'middle_initial': client.middle_initial,
        'last_name': client.last_name, 'client_number': client.client_number,
        'business_name': client.business_name, 'is_business': client.is_business,
        'client_date': client.client_date
    }

    # Post
    if request.method =='POST':
        form_list[0] = ClientForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ClientForm(request.POST)
        validation = validation_helper(form_list)

        if validation:
            a = update_address_helper(request, address)
            c = update_contact_helper(request, contact)
            cl = update_client_helper(request, a, c)
            return HttpResponseRedirect(reverse('Client:index'))

    else:
        form_list[0] = ClientForm(client_dict)
        form_list[1] = AddressForm(address_dict)
        form_list[2] = ContactForm(contact_dict)
    form_dict = dict_generator(form_list)
    return render(request, 'client/editclient.html', form_dict)


"""
class EditClientView(View):
    form_class = Client
    template_name = 'client/editclient.html'
    form_list = form_generator(3)
    client_id = 'pk'
    # Get data
    client = Client.objects.get(pk=client_id)
    address = Address.objects.get(pk=client.client_address_id)
    contact = Contact.objects.get(pk=client.client_contact_id)
    # Create dictionaries to bind to forms
    address_dict = {
        'street': address.street, 'unit': address.unit, 'city': address.city,
        'state': address.state, 'zip_code': address.zip_code
    }
    contact_dict = {
        'phone': contact.phone, 'phone_extension': contact.phone_extension,
        'cell': contact.cell, 'email': contact.email, 'website': contact.website,
        'work_email': contact.work_email, 'office_phone': contact.office_phone,
        'office_phone_extension': contact.office_phone_extension
    }
    client_dict = {
        'first_name': client.first_name, 'middle_initial': client.middle_initial,
        'last_name': client.last_name, 'client_number': client.client_number,
        'business_name': client.business_name, 'is_business': client.is_business,
        'client_date': client.client_date
    }

    # Post
    def post(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = ClientForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ClientForm(request.POST)
        validation = validation_helper(form_list)

        if validation:
            a = update_address_helper(request, address)
            c = update_contact_helper(request, contact)
            cl = update_client_helper(request, a, c)
            return HttpResponseRedirect(reverse('Client:index'))

    def get(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = ClientForm(client_dict)
        form_list[1] = AddressForm(address_dict)
        form_list[2] = ContactForm(contact_dict)
        form_dict = dict_generator(form_list)
        return render(request, 'client/editclient.html', form_dict)
"""

#endregion

#region Billing Views


def addbilling(request, client_id):
    pass
    #TODO Create view to add billing information

#endregion
