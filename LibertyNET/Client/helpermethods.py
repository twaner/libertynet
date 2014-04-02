from models import Client, SalesProspect, SalesProspectCallLog, ClientCallLog
from Common.helpermethods import boolean_helper
from Employee.models import Employee
from Site.models import Site

#region Client


def create_client_helper(form, address, contact):
    """
    Takes a request, and FK objects and creates a new client.
    @param request: request.
    @param args: Address, Contact
    @return:
    """
    first_name = form.cleaned_data.get('first_name')
    last_name = form.cleaned_data.get('last_name')
    middle_initial = form.cleaned_data.get('middle_initial')
    client_number = form.cleaned_data.get('client_number')
    business_name = form.cleaned_data.get('business_name')
    is_business = boolean_helper(form.cleaned_data.get('is_business'))
    client_date = form.cleaned_data.get('client_date')

    client = Client.objects.create_client(first_name=first_name, middle_initial=middle_initial,
                                          last_name=last_name, client_number=client_number,
                                          business_name=business_name, is_business=is_business,
                                          client_address=address, client_contact=contact,
                                          client_date=client_date)
    # Create Client's Site
    site = Site.objects.create_client_site(client)

    return client


def update_client_helper(form, client, address, contact):
    #client.client_date does not change
    #client.client_number does not change
    client.first_name = form.cleaned_data.get('first_name')
    client.middle_initial = form.cleaned_data.get('middle_initial')
    client.last_name = form.cleaned_data.get('last_name')
    client.business_name = form.cleaned_data.get('business_name')
    client.is_business = boolean_helper(form.cleaned_data.get('is_business'))
    client.client_date = form.cleaned_data.get('client_date')
    client.client_number = form.cleaned_data.get('client_number')
    client.client_address = address
    client.client_contact = contact
    """
    client.save(update_fields=['first_name', 'middle_initial', 'last_name', 'business_name', 'is_business',
                               'client_address', 'client_contact'])
    """
    client.save(update_fields=['first_name', 'middle_initial',
                               'last_name', 'client_number',
                               'business_name', 'is_business',
                               'client_address', 'client_contact',
                               'client_date'])

    client.save()
    return client


def update_client_billing_helper(client, billing):
    """
    Updates a Client's Billing Information
    @type client: Client.
    @param client: Client.
    @param billing: Billing.
    @return: Client.
    """
    client.client_billing = billing
    client.save()
    return client


#endregion

#region Sales_Prospect


def create_sales_prospect_helper(form, address, contact):
    first_name = form.cleaned_data.get('first_name')
    middle_initial = form.cleaned_data.get('middle_initial')
    last_name = form.cleaned_data.get('last_name')
    sp_liberty_contact = None
    pk = form.cleaned_data.get('sp_liberty_contact')
    if pk is not None:
        try:
            sp_liberty_contact = Employee.objects.get(employee_id=pk.employee_id)
        except ValueError:
            pass
    sp_business_name = form.cleaned_data.get('sp_business_name')
    if sp_business_name == '' or sp_business_name is None:
        sp_business_name = None
    is_business = boolean_helper(form.cleaned_data.get('is_business'))
    if is_business is None or is_business == '':
        is_business = False

    sales_type = form.cleaned_data.get('sales_type')
    sales_probability = form.cleaned_data.get('sales_probability')
    initial_contact_date = form.cleaned_data.get('initial_contact_date')
    comments = form.cleaned_data.get('comments')

    sales_prospect = SalesProspect.objects.create_sales_prospect(first_name=first_name, middle_initial=middle_initial,
                                                                 last_name=last_name,
                                                                 sp_liberty_contact=sp_liberty_contact,
                                                                 sp_business_name=sp_business_name,
                                                                 is_business=is_business,
                                                                 sales_type=sales_type,
                                                                 sales_probability=sales_probability,
                                                                 initial_contact_date=initial_contact_date,
                                                                 sp_address=address,
                                                                 sp_contact=contact, comments=comments)
    sales_prospect.save()
    return sales_prospect


def update_sales_prospect_helper(form, sp, address, contact):
    sp.first_name = form.cleaned_data.get('first_name')
    sp.middle_initial = form.cleaned_data.get('middle_initial')
    sp.last_name = form.cleaned_data.get('last_name')
    sp.sales_type = form.cleaned_data.get('sales_type')
    sp.sales_probability = form.cleaned_data.get('sales_probability')
    sp.comments = form.cleaned_data.get('comments')
    sp.is_client = form.cleaned_data.get('is_client')
    #Logic section
    if address is not None:
        sp.sp_address = address
    if contact is not None:
        sp.sp_contact = contact

    sp.sp_business_name = form.cleaned_data.get('sp_business_name')
    if sp.sp_business_name == '' or sp.sp_business_name is None:
        sp.sp_business_name = None

    sp.is_business = boolean_helper(form.cleaned_data.get('is_business'))
    sp.sp_liberty_contact = None
    pk = form.cleaned_data.get('sp_liberty_contact')
    if pk is not None:
        try:
            sp.sp_liberty_contact = Employee.objects.get(employee_id=pk.employee_id)
        except ValueError:
            pass
    sp.is_client = boolean_helper(form.cleaned_data.get('is_client'))

    sp.save(update_fields=['first_name', 'middle_initial',
                           'last_name', 'sp_liberty_contact',
                           'sp_business_name', 'is_business',
                           'sales_type', 'sales_probability',
                           'initial_contact_date', 'sp_address',
                           'sp_contact', 'comments', 'is_client'])
    return sp


#endregion

#region CallLogs


def create_calllog_helper(form, obj):
    caller = Employee.objects.get(pk=form.cleaned_data.get('caller').employee_id)
    call_date = form.cleaned_data.get('call_date')
    call_time = form.cleaned_data.get('call_time')
    purpose = form.cleaned_data.get('purpose')
    notes = form.cleaned_data.get('notes')
    next_contact = form.cleaned_data.get('next_contact')

    if isinstance(obj, Client):
        client_id = obj
        calllog = ClientCallLog.objects.create_client_calllog(client_id=client_id, caller=caller, call_date=call_date,
                                                              call_time=call_time, purpose=purpose, notes=notes,
                                                              next_contact=next_contact)
        return calllog
    elif isinstance(obj, SalesProspect):
        sales_id = obj
        calllog = SalesProspectCallLog.objects.create_sales_calllog(sales_id=sales_id, caller=caller,
                                                                    call_date=call_date, call_time=call_time,
                                                                    purpose=purpose, notes=notes,
                                                                    next_contact=next_contact)
        return calllog


        #endregion