from trace import Trace
from django.views.decorators.csrf import csrf_protect
from django.contrib.gis.db.backends.spatialite import client
from django.core.context_processors import request
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.template.context import RequestContext
from django.views.generic import ListView, DetailView, UpdateView
from django.views.generic.base import View
from datetime import date, datetime
from models import Client, SalesProspect, ClientCallLog, SalesProspectCallLog
from helpermethods import create_client_helper, create_sales_prospect_helper, update_client_helper, \
    update_sales_prospect_helper, create_calllog_helper, create_client_calllog_helper, create_sales_calllog_helper, \
    update_call_log_helper
from forms import ClientForm, SalesProspectForm, SalesProspectEditForm, SalesProspectCallLogForm, ClientCallLogForm, ClientForm2
from Common.forms import AddressForm, ContactForm
from Common.models import Address, Contact, Billing
from Common.helpermethods import create_address_helper, form_generator, create_contact_helper, \
    validation_helper, dict_generator, update_address_helper, update_contact_helper, boolean_helper
from Site.models import Site
import operator

#region ListViews - Index Views of All of an Object


class ClientListView(ListView):
    """
    View of all Clients, Clients sorted by client_date.
    """
    model = Client
    context_object_name = 'all_client_list'
    template_name = 'client/index.html'
    #context = RequestContext(request)

    def get_context_data(self, **kwargs):
        context = super(ClientListView, self).get_context_data(**kwargs)

        sorted_list = sorted(context['object_list'], key=lambda client: client.client_date)

        if len(sorted_list) <= 5:
            q = len(sorted_list)
        else:
            q = len(sorted_list) - 4
        context['most_recent'] = sorted_list[q:]
        # Clients that are marked for follow up in call log => Client should appear once only
        calllog = ClientCallLog.objects.filter(follow_up=True)
        #tmp_list = [calllog.client_id for calllog.client_id in calllog]
        tmp_list = [Client.objects.get(pk=q.client_id.client_id) for q in calllog]
        context['follow_up'] = set(tmp_list)
        context['calllog_follow_all'] = calllog

        return context


class SalesProspectListView(ListView):
    """
    View to List all Sales Prospects
    """
    model = SalesProspect
    context_object_name = 'all_sales_prospect_list'
    template_name = 'client/salesprospectindex.html'

    def get_context_data(self, **kwargs):
        context = super(SalesProspectListView, self).get_context_data(**kwargs)

        try:
            context['all_sales_prospect_list'] = SalesProspect.objects.filter(is_business=False)
        except SalesProspect.DoesNotExist:
            pass
        sorted_list = []
        tmp_list = []
        sorted_list = sorted(context['all_sales_prospect_list'],
                             key=lambda sales_prospect: sales_prospect.initial_contact_date)
        if len(sorted_list) <= 5:
            q = len(sorted_list)
        else:
            q = len(sorted_list) - 4
        context['most_recent'] = sorted_list[q:]

        calllog = SalesProspectCallLog.objects.filter(follow_up=True)
        try:
            tmp_list = [SalesProspect.objects.get(pk=q.sales_id.id, is_business=False) for q in calllog]
        except SalesProspect.DoesNotExist:
            pass
        context['follow_up'] = set(tmp_list)
        context['calllog_follow_all'] = calllog

        return context


class ClientCallLogHome(ListView):
    """
    View to list all Client Calls
    """
    model = ClientCallLog
    template_name = 'client/callloghome.html'
    context_object_name = 'calllog'

    def get_context_data(self, **kwargs):
        context = super(ClientCallLogHome, self).get_context_data(**kwargs)
        context['calllog_list'] = ClientCallLog.objects.all().order_by('-call_date', '-call_time')
        return context


class SalesCallLogHome(ListView):
    """
    View for Sales Prospect Call Logs
    """
    model = SalesProspectCallLog
    template_name = 'client/salescallloghome.html'
    context_object_name = 'calllog'

    # def get_context_data(self, **kwargs):
    #     context = super(SalesProspectCallLog, self).get_context_data(self, **kwargs)
    #     return context

#region DetailViews - Details for an Object.


class ClientDetailView(DetailView):
    """
    View for Client Details.
    """
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
            context['billing_detail'] = Billing.objects.filter(pk=client.client_billing_id)
        except ObjectDoesNotExist:
            pass
        try:
            context['site_detail'] = Site.objects.filter(site_client_id=client.client_id)
        except ObjectDoesNotExist:
            pass
        try:
            context['calllog_list'] = ClientCallLog.objects.filter(client_id=client.client_id).\
                order_by('-call_date', '-call_time')
            context['calllog_follow'] = ClientCallLog.objects.filter(client_id=client.client_id).\
                filter(follow_up=True)
            context['next_contact'] = ClientCallLog.objects.get_next_contact_date(client)
        except ObjectDoesNotExist:
            pass
        return context


class ClientDetailViewWO(DetailView):
    """
    View for Client Details.
    """
    model = Client
    client_id = 'pk'
    context_object_name = 'client_detail'
    template_name = 'client/clientdetails.html'

    def get_context_data(self, **kwargs):
        context = super(ClientDetailViewWO, self).get_context_data(**kwargs)
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
    """
    View for Sales Prospect Details.
    """
    model = SalesProspect
    id = 'pk'
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
                filter(sales_id=sales.id)
        except SalesProspectCallLog.DoesNotExist:
            pass
        return context


class SalesProspectDetailViewWrap(DetailView):
    """
    View for Sales Prospect Details.
    """
    model = SalesProspect
    id = 'pk'
    template_name = 'client/salesdetails_wrap.html'
    context_object_name = 'sales_prospect_detail'

    def get_context_data(self, **kwargs):
        context = super(SalesProspectDetailViewWrap, self).get_context_data(**kwargs)
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
                filter(sales_id=sales.id)
        except SalesProspectCallLog.DoesNotExist:
            pass
        return context


#endregion

#region AddViews - Views for creating an Object.


class SalesProspectView(View):
    """
    View to Add Sales Prospect.
    """
    form_class = SalesProspect
    template_name = 'client/addsalessprospect.html'
    form_list = form_generator(3)

    def post(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = SalesProspectForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address = create_address_helper(form_list[1])
            contact = create_contact_helper(form_list[2])
            sales_prospect = create_sales_prospect_helper(request, address=address, contact=contact)
            return HttpResponseRedirect(reverse('Client:salesprospectdetails',
                                                kwargs={'pk': sales_prospect.id}))
        else:
            return render(request, self.template_name, dict_generator(form_list))

    def get(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = SalesProspectForm()
        form_list[1] = AddressForm()
        form_list[2] = ContactForm()
        form_dict = dict_generator(form_list)
        return render(request, self.template_name, form_dict)


class ClientView(View):
    """
    View to Add a new Client.
    """
    form_class = Client
    template_name = 'client/addclient.html'
    form_list = form_generator(3)

    def post(self, request, form_list=form_list, *args, **kwargs):
        form_list[0] = ClientForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = ContactForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address = create_address_helper(form_list[1])
            contact = create_contact_helper(form_list[2])
            client = create_client_helper(form_list[0], address, contact)
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
    """
    View to Edit a Sales Prospect
    @param request: request.
    @param pk: pk of Sales obj.
    @return: http.
    """
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
            address_up = update_address_helper(form_list[1], address)
            contact_up = update_contact_helper(form_list[2], contact)

            sales_up = update_sales_prospect_helper(form_list[0], sales, address_up, contact_up)

            sp_to_client = boolean_helper(sales_up.is_client)
            if sp_to_client:
                #TODO -- Add manner to send to edit client with dictionaries.
                return HttpResponseRedirect(reverse('Client:salestoclient',
                                                    kwargs={'pk': sales_up.id}))
            return HttpResponseRedirect(reverse('Client:salesprospectdetails',
                                                kwargs={'pk': sales_up.id}))
        else:
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = SalesProspectEditForm(sales_dict)
        form_list[1] = AddressForm(address_dict)
        form_list[2] = ContactForm(contact_dict)
    form_dict = dict_generator(form_list)
    form_dict['sales'] = sales
    return render(request, template_name, form_dict)


def convert_to_client(request, pk):
    """
    View to convert a SalesProspect to a Client.
    @param request: request.
    @param pk: Sales PK.
    @return: http.
    """
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
            a = update_address_helper(form_list[1], address)
            c = update_contact_helper(form_list[2], contact)
            cl = update_client_helper(form_list[0], client, a, c)
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

@login_required
def editclient(request, pk):
    """
    View to edit a Client.
    @param request: request.
    @param pk: Client PK.
    @return: http.
    """
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
            a = update_address_helper(form_list[1], address)
            c = update_contact_helper(form_list[2], contact)
            cl = update_client_helper(form_list[0], client, a, c)
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

class ClientCallLogView(View):
    """
    Creates a Client Call Log for any Client.
    @return: http response.
    """
    form_class = ClientCallLog
    template_name = 'client/addcalllog.html'
    form_list = form_generator(1)
    calllog_dict = {
        'call_date': date.today().strftime("%Y-%m-%d"),
        'call_time': datetime.now().time().strftime("%H:%M"),
    }

    def post(self, request, form_list=form_list, calllog_dict=calllog_dict, *args, **kwargs):
        form_list[0] = ClientCallLogForm(request.POST)

        if validation_helper(form_list):
            calllog = create_client_calllog_helper(form_list[0])
            return HttpResponseRedirect(reverse('Client:details', kwargs={'pk': calllog.client_id.client_id}))
        else:
            form_list[0] = ClientCallLogForm(calllog_dict)
            return render(request, self.template_name, dict_generator(form_list))

    def get(self, request, form_list=form_list, calllog_dict=calllog_dict, *args, **kwargs):
        form_list[0] = ClientCallLogForm(calllog_dict)
        return render(request, self.template_name, dict_generator(form_list))

@login_required
def addclientcalllog(request, pk):
    """
    Creates a Call Log for a Client based on pk that is passed in.
    @param request: request.
    @param pk: pk for Client.
    @return: http response.
    """
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
            calllog = create_calllog_helper(form_list[0], client)
            return HttpResponseRedirect(reverse('Client:details', kwargs={'pk': client.client_id}))
        else:
            form_list[0] = ClientCallLogForm(calllog_dict)
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = ClientCallLogForm(calllog_dict)
        fd = dict_generator(form_list)
        fd['client'] = client
        return render(request, template_name, fd)


def followupcall(request, pk):
    """
    Creates a Call Log for a Client based on pk that is passed in.
    @param request: request.
    @param pk: pk for Client.
    @return: http response.
    """
    template_name = 'client/addclientcalllog.html'
    form_list = form_generator(1)
    call = ClientCallLog.objects.get(pk=pk)
    client = call.client_id
    calllog_dict = {
        'client_id': call.client_id, 'call_date': date.today().strftime("%Y-%m-%d"),
        'call_time': datetime.now().time().strftime("%H:%M"), 'purpose': 'Follow Up: ' + call.purpose,
    }
    #Update purpose field
    #calllog_dict['purpose'] = 'Follow Up: '

    if request.method == 'POST':
        form_list[0] = ClientCallLogForm(request.POST)
        if validation_helper(form_list):
            calllog = create_calllog_helper(form_list[0], client)
            #Update previous call
            call.follow_up = False
            call.save()
            return HttpResponseRedirect(reverse('Client:details', kwargs={'pk': client.client_id}))
        else:
            form_list[0] = ClientCallLogForm(calllog_dict)
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = ClientCallLogForm(calllog_dict)
        fd = dict_generator(form_list)
        fd['client'] = call.client_id
        return render(request, template_name, fd)


def editclientcall(request, pk):
    """
    View to edit a Client CallLog.
    @param request: request.
    @param pk: Pk of CallLog.
    @return: Http.
    """
    template_name = 'client/editclientcall.html'
    form_list = form_generator(1)
    calllog = ClientCallLog.objects.get(pk=pk)
    print('editclientcall: REQUEST %s' % request.get_full_path())
    calllog_dict = {
        'caller': calllog.caller, 'call_date': calllog.call_date.strftime("%Y-%m-%d"),
        'call_time': calllog.call_time.strftime("%H:%M"), 'purpose': calllog.purpose,
        'notes': calllog.notes, 'next_contact': calllog.next_contact,
        'follow_up': calllog.follow_up, 'client_id': calllog.client_id,
    }

    if request.method == 'POST':
        form_list[0] = ClientCallLogForm(request.POST)
        if validation_helper(form_list):
            calllog = update_call_log_helper(form_list[0], calllog)
            return HttpResponseRedirect(reverse('Client:clientcalllogdetails',
                                                kwargs={'pk': calllog.id}))
        else:
            form_list[0] = ClientCallLogForm(calllog_dict)
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = ClientCallLogForm(calllog_dict)
        form_dict = dict_generator(form_list)
        form_dict['call'] = calllog
        return render(request, template_name, form_dict)


class EditClientCall(UpdateView):
    model = ClientCallLog
    fields = ['caller', 'purpose', 'notes', 'follow_up']
    template_name_suffix = '_update_form'


class CallLogDetailView(DetailView):
    """
    Client Call Log Detail View.
    """
    model = ClientCallLog
    client_id = 'pk'
    template_name = 'client/clientcalllogdetails.html'
    context_object_name = 'calllog'

    def get_context_data(self, **kwargs):
        context = super(CallLogDetailView, self).get_context_data(**kwargs)
        return context


class ClientCallLogIndex(DetailView):
    """
    CallLog index view for Client.
    """
    model = Client
    client_id = 'pk'
    template_name = 'client/clientcalllogindex.html'
    context_object_name = 'client'

    def get_context_data(self, **kwargs):
        context = super(ClientCallLogIndex, self).get_context_data(**kwargs)
        client = self.get_object()
        context['calllog_list'] = ClientCallLog.objects.filter(client_id=client.client_id)\
            .order_by('-call_date', 'call_time')
        context['next_contact'] = ClientCallLog.objects.get_next_contact_date(client)

        return context


def addsalescall(request, pk):
    """
    View to add a SalesProspect CallLog.
    @param request: request.
    @param pk: Sales PK.
    @return: http.
    """
    template_name = 'client/addsalescall.html'
    form_list = form_generator(1)
    form_list[0] = SalesProspectCallLogForm(request.POST)
    sales = SalesProspect.objects.get(pk=pk)
    calllog_dict = {
        'sales_id': sales.id, 'call_date': date.today().strftime("%Y-%m-%d"),
        'call_time': datetime.now().time().strftime("%H:%M"),
    }

    if request.method == 'POST':
        if validation_helper(form_list):
            calllog = create_calllog_helper(form_list[0], sales)
            return HttpResponseRedirect(reverse('Client:salesprospectdetails', kwargs={'pk': sales.id}))
        else:
            form_list[0] = SalesProspectCallLogForm(calllog_dict)
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = SalesProspectCallLogForm(calllog_dict)
        fd = dict_generator(form_list)
        fd['sales'] = sales
        return render(request, template_name, fd)


class SalesCallLogDetailView(DetailView):
    """
    SalesProspect CallLog detail view.
    """
    model = SalesProspectCallLog
    client_id = 'pk'
    template_name = 'client/salescalllogdetails.html'
    context_object_name = 'calllog'

    def get_context_data(self, **kwargs):
        context = super(SalesCallLogDetailView, self).get_context_data(**kwargs)
        return context


class SalesCallLogIndex(DetailView):
    """
    SalesProspect CallLog index view.
    """
    model = SalesProspect
    sales_id = 'pk'
    template_name = 'client/salescalllogindex.html'
    context_object_name = 'sales'

    def get_context_data(self, **kwargs):
        context = super(SalesCallLogIndex, self).get_context_data(**kwargs)
        sales = self.get_object()
        context['calllog_list'] = SalesProspectCallLog.objects.filter(sales_id=sales.id)\
            .order_by('-call_date', '-call_time')
        context['next_contact'] = SalesProspectCallLog.objects.get_next_contact_date(sales)

        return context


def editsalescall(request, pk):
    pass
    template_name = 'client/editclientcall.html'
    form_list = form_generator(1)
    calllog = ClientCallLog.objects.get(pk=pk)
    calllog_dict = {
        'caller': calllog.caller, 'call_date': calllog.call_date.strftime("%Y-%m-%d"),
        'call_time': calllog.call_time.strftime("%H:%M"), 'purpose': calllog.purpose,
        'notes': calllog.notes, 'next_contact': calllog.next_contact,
        'follow_up': calllog.follow_up, 'client_id': calllog.client_id,
    }

    if request.method == 'POST':
        form_list[0] = ClientCallLogForm(request.POST)
        if validation_helper(form_list):
            calllog = update_call_log_helper(form_list[0], calllog)
            return HttpResponseRedirect(reverse('Client:clientcalllogdetails',
                                                kwargs={'pk': calllog.id}))
        else:
            form_list[0] = ClientCallLogForm(calllog_dict)
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = ClientCallLogForm(calllog_dict)
        form_dict = dict_generator(form_list)
        form_dict['call'] = calllog
        return render(request, template_name, form_dict)

#endregion