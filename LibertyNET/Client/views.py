from django.core.context_processors import request
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from datetime import date, datetime
from models import Client, SalesProspect, ClientCallLog, SalesProspectCallLog
from helpermethods import create_client_helper, create_sales_prospect_helper, update_client_helper, \
    update_sales_prospect_helper, create_calllog_helper
from forms import ClientForm, SalesProspectForm, SalesProspectEditForm, SalesProspectCallLogForm, ClientCallLogForm
from Common.forms import AddressForm, ContactForm
from Common.models import Address, Contact, Billing
from Common.helpermethods import create_address_helper, form_generator, create_contact_helper, \
    validation_helper, dict_generator, update_address_helper, update_contact_helper, boolean_helper
from Site.models import Site

#region ListViews


class ClientListView(ListView):
    model = Client
    context_object_name = 'all_client_list'
    template_name = 'client/index.html'


class SalesProspectListView(ListView):
    model = SalesProspect
    context_object_name = 'all_sales_prospect_list'
    template_name = 'client/salesprospectindex.html'

#region DetailViews


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
        #if client.client_billing_id is not None:
        try:
            context['billing_detail'] = Billing.objects.get(pk=client.client_billing_id)
        except ObjectDoesNotExist:
            pass
        try:
            context['site_detail'] = Site.objects.get(site_client_id=client.client_id)
        except ObjectDoesNotExist:
            pass
        return context


class SalesProspectDetailView(DetailView):
    model = SalesProspect
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
        try:
            context['call_detail'] = SalesProspectCallLog.objects.\
                filter(sales_id=sales.sales_prospect_id)
        except SalesProspectCallLog.DoesNotExist:
            pass
        return context

#endregion

#region AddViews


class SalesProspectView(View):
    form_class = SalesProspect
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
            return HttpResponseRedirect(reverse('Client:salesprospectdetails',
                                                kwargs={'pk': sales_prospect.sales_prospect_id}))
        else:
            return render(request, self.template_name, dict_generator(form_list))

    def get(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = SalesProspectForm()
        form_list[1] = AddressForm()
        form_list[2] = ContactForm()
        form_dict = dict_generator(form_list)
        return render(request, self.template_name, form_dict)


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
            return HttpResponseRedirect(reverse('Client:details',
                                                kwargs={'pk': client.client_id}))
        else:
            return render(request, self.template_name, dict_generator(form_list))

    def get(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = ClientForm()
        form_list[1] = AddressForm()
        form_list[2] = ContactForm()
        form_dict = dict_generator(form_list)
        return render(request, self.template_name, form_dict)


#endregion

#region EditViews


def editsalesprospect(request, pk):
    template_name = 'client/editsalesprospect.html'
    form_list = form_generator(3)
    sales = SalesProspect.objects.get(pk=pk)
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
        'initial_contact_date': sales.initial_contact_date, 'comments': sales.comments,
        'is_client': sales.is_client
    }
    if request.method == 'POST':
        form_list[0] = SalesProspectEditForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address_up = update_address_helper(request, address)
            contact_up = update_contact_helper(request, contact)

            sales_up = update_sales_prospect_helper(request, sales, address_up, contact_up)

            sp_to_client = boolean_helper(sales_up.is_client)
            if sp_to_client:
                #TODO -- Add manner to send to edit client with dictionaries.
                return HttpResponseRedirect(reverse('Client:salestoclient',
                                                    kwargs={'pk': sales_up.sales_prospect_id}))
            return HttpResponseRedirect(reverse('Client:salesprospectdetails',
                                                kwargs={'pk': sales_up.sales_prospect_id}))
        else:
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = SalesProspectEditForm(sales_dict)
        form_list[1] = AddressForm(address_dict)
        form_list[2] = ContactForm(contact_dict)
    form_dict = dict_generator(form_list)
    return render(request, template_name, dict_generator(form_list))


def convert_to_client(request, pk):
    pass
    template_name = 'client/salestoclient.html'
    form_list = form_generator(3)
    sp = SalesProspect.objects.get(pk=pk)
    contact = Contact.objects.get(pk=sp.sp_contact_id)
    try:
        address = Address.objects.get(pk=sp.sp_address_id)
    except ObjectDoesNotExist:
        address = None
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
    # Create client for use with dictionary
    client = Client()
    client_dict = {
        'first_name': sp.first_name, 'middle_initial': sp.middle_initial,
        'last_name': sp.last_name, 'client_number': '',
        'business_name': sp.sp_business_name, 'is_business': sp.is_business,
        'client_date': date.today().strftime("%Y-%m-%d")
    }

    if request.method == 'POST':
        form_list[0] = ClientForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)
        validation = validation_helper(form_list)

        if validation:
            a = update_address_helper(request, address)
            c = update_contact_helper(request, contact)
            cl = update_client_helper(request, client, a, c)
            return HttpResponseRedirect(reverse('Client:details',
                                                kwargs={'pk': cl.client_id}))
        else:
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = ClientForm(client_dict)
        form_list[1] = AddressForm(address_dict)
        form_list[2] = ContactForm(contact_dict)
    form_dict = dict_generator(form_list)
    return render(request, template_name, form_dict)


def editclient(request, pk):
    template_name = 'client/editclient.html'
    form_list = form_generator(3)
    client = Client.objects.get(pk=pk)
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
    if request.method == 'POST':
        form_list[0] = ClientForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)
        validation = validation_helper(form_list)

        if validation:
            a = update_address_helper(request, address)
            c = update_contact_helper(request, contact)
            cl = update_client_helper(request, client, a, c)
            return HttpResponseRedirect(reverse('Client:details',
                                                kwargs={'pk': cl.client_id}))

    else:
        form_list[0] = ClientForm(client_dict)
        form_list[1] = AddressForm(address_dict)
        form_list[2] = ContactForm(contact_dict)
    form_dict = dict_generator(form_list)
    return render(request, template_name, form_dict)

#endregion


#region CallLogs


def addclientcalllog(request, pk):
    template_name = 'client/addclientcalllog.html'
    form_list = form_generator(1)
    form_list[0] = ClientCallLogForm(request.POST)
    client = Client.objects.get(pk=pk)
    calllog_dict = {
        'client_id': client.client_id, 'call_date': date.today().strftime("%Y-%m-%d"),
        'call_time': datetime.now().time().strftime("%H:%M"),
    }

    if request.method == 'POST':
        if validation_helper(form_list):
            calllog = create_calllog_helper(request, client)
            return HttpResponseRedirect(reverse('Client:details', kwargs={'pk': client.client_id}))
        else:
            form_list[0] = ClientCallLogForm(calllog_dict)
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = ClientCallLogForm(calllog_dict)
        return render(request, template_name, dict_generator(form_list))


class CallLogDetailView(DetailView):
    model = ClientCallLog
    client_id = 'pk'
    template_name = 'client/clientcalllogdetails.html'
    context_object_name = 'calllog'

    def get_context_data(self, **kwargs):
        context = super(CallLogDetailView, self).get_context_data(**kwargs)
        return context


class ClientCallLogIndex(DetailView):
    model = Client
    client_id = 'pk'
    template_name = 'client/clientcalllogindex.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super(ClientCallLogIndex, self).get_context_data(**kwargs)
        client = self.get_object()
        context['calllog_list'] = ClientCallLog.objects.filter(client_id=client.client_id)\
            .order_by('call_date', 'call_time')
        context['next_contact'] = ClientCallLog.objects.get_next_contact_date(client)

        return context


def addsalescalllog(request, pk):
    template_name = 'client/addsalescalllog.html'
    form_list = form_generator(1)
    form_list[0] = SalesProspectCallLogForm(request.POST)
    sales = SalesProspect.objects.get(pk=pk)
    calllog_dict = {
        'sales_id': sales.sales_prospect_id, 'call_date': date.today().strftime("%Y-%m-%d"),
        'call_time': datetime.now().time().strftime("%H:%M"),
    }

    if request.method == 'POST':
        if validation_helper(form_list):
            calllog = create_calllog_helper(request, sales)
            return HttpResponseRedirect(reverse('Client:salesprospectdetails', kwargs={'pk': sales.sales_prospect_id}))
        else:
            form_list[0] = SalesProspectCallLogForm(calllog_dict)
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = SalesProspectCallLogForm(calllog_dict)
        return render(request, template_name, dict_generator(form_list))


class SalesCallLogDetailView(DetailView):
    model = SalesProspectCallLog
    client_id = 'pk'
    template_name = 'client/salescalllogdetails.html'
    context_object_name = 'calllog'

    def get_context_data(self, **kwargs):
        context = super(SalesCallLogDetailView, self).get_context_data(**kwargs)
        return context


class SalesCallLogIndex(DetailView):
    model = SalesProspect
    sales_id = 'pk'
    template_name = 'client/salescalllogindex.html'
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super(SalesCallLogIndex, self).get_context_data(**kwargs)
        sales = self.get_object()
        context['calllog_list'] = SalesProspectCallLog.objects.filter(sales_id=sales.sales_prospect_id)\
            .order_by('call_date', 'call_time')
        context['next_contact'] = SalesProspectCallLog.objects.get_next_contact_date(sales)

        return context


#endregion
