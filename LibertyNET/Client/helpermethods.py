from mock import call
from models import Client, SalesProspect, SalesProspectCallLog, ClientCallLog
from Common.helpermethods import boolean_helper
from Employee.models import Employee
from Site.models import Site
from datetime import date, datetime

#region Client


def create_client_helper(form, *args):
    """
    Takes a form, and FK objects and creates a new client.
    @param form: request.
    @param args: Address, Contact
    @return:
    """
    first_name = form.cleaned_data['first_name']
    last_name = form.cleaned_data['last_name']
    middle_initial = form.cleaned_data['middle_initial']
    client_number = form.cleaned_data['client_number']
    business_name = form.cleaned_data['business_name']
    is_business = boolean_helper(form.cleaned_data['is_business'])
    client_date = form.cleaned_data['client_date']

    client = Client.objects.create_client(first_name=first_name, middle_initial=middle_initial,
                                          last_name=last_name, client_number=client_number,
                                          business_name=business_name, is_business=is_business,
                                          client_address=args[0], client_contact=args[1],
                                          client_date=client_date)
    # Create Client's Site
    # This will default to either
    if boolean_helper(is_business):
        site_name = business_name
    else:
        site_name = 'Home'
    site = Site.objects.create_client_site(client, args[0], site_name)

    return client


def update_client_helper(form, client, address, contact):
    #client.client_date does not change
    #client.client_number does not change
    """
    Updates a Client Object.
    @param form: Client Form.
    @param client: Client.
    @param address: Address Object.
    @param contact: Contact.
    @return: Updated Client.
    """
    client.first_name = form.cleaned_data['first_name']
    client.middle_initial = form.cleaned_data['middle_initial']
    client.last_name = form.cleaned_data['last_name']
    client.business_name = form.cleaned_data['business_name']
    client.is_business = boolean_helper(form.cleaned_data['is_business'])
    client.client_date = form.cleaned_data['client_date']
    client.client_number = form.cleaned_data['client_number']
    client.client_address = address
    client.client_contact = contact
    """
    client.save(update_fields=['first_name', 'middle_initial', 'last_name', 'business_name', 'is_business',
                               'client_address', 'client_contact'])
    """
    client.save()
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
    """
    Creates a Sales Prospect Object.
    @param form: Sales Prospect form.
    @param address: Address Object.
    @param contact: Contact Object.
    @return:
    """
    first_name = form.cleaned_data['first_name']
    middle_initial = form.cleaned_data['middle_initial']
    last_name = form.cleaned_data['last_name']
    try:
        sp_liberty_contact = Employee.objects.get(pk=form.cleaned_data['sp_liberty_contact'])
    except ValueError:
        sp_liberty_contact = None

    sp_business_name = form.cleaned_data['sp_business_name']
    if sp_business_name == '' or sp_business_name is None:
        sp_business_name = None

    is_business = boolean_helper(form.cleaned_data['is_business'])
    if is_business is None or is_business == '':
        is_business = False

    sales_type = form.cleaned_data['sales_type']
    sales_probability = form.cleaned_data['sales_probability']
    initial_contact_date = form.cleaned_data['initial_contact_date']
    comments = form.cleaned_data['comments']
    service_guide = form.cleaned_data['service_guide']

    sales_prospect = SalesProspect.objects.create_sales_prospect(first_name=first_name, middle_initial=middle_initial,
                                                                 last_name=last_name,
                                                                 sp_liberty_contact=sp_liberty_contact,
                                                                 sp_business_name=sp_business_name,
                                                                 is_business=is_business,
                                                                 sales_type=sales_type,
                                                                 sales_probability=sales_probability,
                                                                 initial_contact_date=initial_contact_date,
                                                                 sp_address=address, service_guide=service_guide,
                                                                 sp_contact=contact, comments=comments)
    sales_prospect.save()
    return sales_prospect


def update_sales_prospect_helper(form, sp, address, contact):
    """
    Updates a Sales Prospect.
    @param form: Sales Prospect form.
    @param sp: Sales Prospect object.
    @param address: Address object.
    @param contact: Contact Object.
    @return:
    """
    sp.first_name = form.cleaned_data['first_name']
    sp.middle_initial = form.cleaned_data['middle_initial']
    sp.last_name = form.cleaned_data['last_name']
    sp.sales_type = form.cleaned_data['sales_type']
    sp.sales_probability = form.cleaned_data['sales_probability']
    sp.comments = form.cleaned_data['comments']
    sp.is_client = form.cleaned_data['is_client']
    sp.service_guide = form.cleaned_data['service_guide']
    #Logic section
    if address is not None:
        sp.sp_address = address
    if contact is not None:
        sp.sp_contact = contact

    sp.sp_business_name = form.cleaned_data['sp_business_name']

    if sp.sp_business_name == '' or sp.sp_business_name is None:
        sp.sp_business_name = None

    sp.is_business = boolean_helper(form.cleaned_data['is_business'])

    try:
        sp.sp_liberty_contact = Employee.objects.get(pk=form.cleaned_data['sp_liberty_contact'].employee_id)
    except ValueError:
        sp.sp_liberty_contact = None

    sp.is_client = boolean_helper(form.cleaned_data['is_client'])

    sp.save(update_fields=['first_name', 'middle_initial',
                           'last_name', 'sp_liberty_contact',
                           'sp_business_name', 'is_business',
                           'sales_type', 'sales_probability',
                           'initial_contact_date', 'sp_address',
                           'sp_contact', 'comments', 'is_client',
                           'service_guide'])
    return sp


#endregion

#region CallLogs


def create_calllog_helper(form, obj):
    """
    Creates a CallLog object for a Client or Sales Prospect.
    @param form: request.
    @param obj: Client or Sales Object.
    @return: CallLog.
    """
    caller = Employee.objects.get(pk=form.cleaned_data['caller'].employee_id)
    call_date = form.cleaned_data['call_date']
    call_time = form.cleaned_data['call_time']
    purpose = form.cleaned_data['purpose']
    notes = form.cleaned_data['notes']
    next_contact = form.cleaned_data['next_contact']
    follow_up = form.cleaned_data['follow_up']

    if isinstance(obj, Client):
        id = obj
        calllog = ClientCallLog.objects.create_client_calllog(id=id, caller=caller, call_date=call_date,
                                                              call_time=call_time, purpose=purpose, notes=notes,
                                                              next_contact=next_contact, follow_up=follow_up)
        return calllog
    elif isinstance(obj, SalesProspect):
        sales_id = obj
        calllog = SalesProspectCallLog.objects.create_sales_calllog(sales_id=sales_id, caller=caller,
                                                                    call_date=call_date, call_time=call_time,
                                                                    purpose=purpose, notes=notes,
                                                                    next_contact=next_contact, follow_up=follow_up)
        return calllog


def create_client_calllog_helper(form):
    """
    Creates a CallLog for a Client without needing a PK.
    @param form: validated form.
    @return: CallLog.
    """
    id = form.cleaned_data['id']
    tmp_emp = form.cleaned_data['caller']
    caller = Employee.objects.get(pk=tmp_emp.employee_id)
    call_date = form.cleaned_data['call_date']
    call_time = form.cleaned_data['call_time']
    purpose = form.cleaned_data['purpose']
    notes = form.cleaned_data['notes']
    next_contact = form.cleaned_data['next_contact']
    follow_up = form.cleaned_data['follow_up']

    calllog = ClientCallLog.objects.create_client_calllog(id=id, caller=caller, call_date=call_date,
                                                          call_time=call_time, purpose=purpose, notes=notes,
                                                          next_contact=next_contact, follow_up=follow_up)
    return calllog


def update_call_log_helper(form, calllog):
    """
    Updates a Client Call Log.
    @param form: form.
    @param calllog: CallLog object.
    @return: CallLog.
    """
    calllog.id = form.cleaned_data['id']
    calllog.caller = form.cleaned_data['caller']
    calllog.call_date = form.cleaned_data['call_date']
    calllog.call_time = form.cleaned_data['call_time']
    calllog.purpose = form.cleaned_data['purpose']
    calllog.follow_up = form.cleaned_data['follow_up']
    calllog.next_contact = form.cleaned_data['next_contact']
    # Notes are appended with date and 'edit'
    # Length of original notes
    old_notes_len = str(calllog.notes).__len__()
    # notes from update.
    new_notes = str(form.cleaned_data['notes'])
    # If new notes is longer add edit
    if old_notes_len != new_notes.__len__():
        calllog.notes = new_notes[0:old_notes_len] + \
                    '\n- Edit - \n [' + date.today().strftime("%Y-%m-%d") + ']' + \
                    new_notes[old_notes_len:-1]
    else:
        calllog.notes = new_notes
    calllog.save(update_fields=['id', 'caller', 'call_date',
                                'call_time', 'purpose', 'follow_up',
                                'next_contact', 'notes'])
    return calllog


def create_sales_calllog_helper(form):
    """
    Creates a CallLog for a Sales without needing a PK.
    @param form: validated form.
    @return: CallLog.
    """
    sales_id = form.cleaned_data['sales_id']
    tmp_emp = form.cleaned_data['caller']
    caller = Employee.objects.get(pk=tmp_emp.employee_id)
    call_date = form.cleaned_data['call_date']
    call_time = form.cleaned_data['call_time']
    purpose = form.cleaned_data['purpose']
    notes = form.cleaned_data['notes']
    next_contact = form.cleaned_data['next_contact']
    follow_up = form.cleaned_data['follow_up']

    calllog = SalesProspectCallLog.objects.create_sales_calllog(sales_id=sales_id, caller=caller,
                                                                call_date=call_date, call_time=call_time,
                                                                purpose=purpose, notes=notes,
                                                                next_contact=next_contact, follow_up=follow_up)
    return calllog

    #endregion