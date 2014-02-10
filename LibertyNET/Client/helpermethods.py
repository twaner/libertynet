from models import Client, Sales_Prospect
from Common.models import Address, Billing, Contact
from Common.helpermethods import boolean_helper
from Employee.models import Employee
from Site.models import Site

#region Client


def create_client_helper(request, *args):
    """
    Takes a request, and FK objects and creates a new client.
    @param request: request.
    @param args: Address, Contact
    @return:
    """
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    middle_initial = request.POST.get('middle_initial')
    client_number = request.POST.get('client_number')
    business_name = request.POST.get('business_name')
    is_business = boolean_helper(request.POST.get('is_business'))
    client_date = request.POST.get('client_date')
    #TODO -- REMOVE CODE
    #client_address = [i for i in args if type(i) == Address]
    #client_contact = [q for q in args if type(q) == Contact]

    client = Client.objects.create(first_name=first_name, middle_initial=middle_initial,
                                   last_name=last_name, client_number=client_number,
                                   business_name=business_name, is_business=is_business,
                                   client_address=args[0], client_contact=args[1],
                                   client_date=client_date)

    site = Site.objects.create_client_site(client)

    return client


def update_client_helper(request, client, address, contact):
    #client.client_date does not change
    #client.client_number does not change
    client.first_name = request.POST.get('first_name')
    client.middle_initial = request.POST.get('middle_initial')
    client.last_name = request.POST.get('last_name')
    client.business_name = request.POST.get('business_name')
    client.is_business = request.POST.get('is_business')
    #ASSUMPTION address, billing, contact will not be None
    client.client_address = address
    client.client_contact = contact

    client.save(update_fields=['first_name', 'middle_initial', 'last_name', 'business_name', 'is_business',
                               'client_address', 'client_contact'])
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


def create_sales_prospect_helper(request, address, contact):
    first_name = request.POST.get('first_name')
    middle_initial = request.POST.get('middle_initial')
    last_name = request.POST.get('last_name')
    try:
        sp_liberty_contact = Employee.objects.get(pk=request.POST.get('sp_liberty_contact'))
    except ValueError:
        sp_liberty_contact = None

    sp_business_name = request.POST.get('sp_business_name')
    if sp_business_name == '' or sp_business_name is None:
        print('NOBUSINESSNAME')
        sp_business_name = None

    is_business = boolean_helper(request.POST.get('is_business'))
    if is_business is None or is_business == '':
        is_business = False

    sales_type = request.POST.get('sales_type')
    sales_probability = request.POST.get('sales_probability')
    initial_contact_date = request.POST.get('initial_contact_date')
    comments = request.POST.get('comments')
    """if len(args) == 2:
        contact = None
    else:
        contact = args[1] """
    sales_prospect = Sales_Prospect.objects.create(first_name=first_name, middle_initial=middle_initial,
                                                   last_name=last_name, sp_liberty_contact=sp_liberty_contact,
                                                   sp_business_name=sp_business_name, is_business=is_business,
                                                   sales_type=sales_type, sales_probability=sales_probability,
                                                   initial_contact_date=initial_contact_date, sp_address=address,
                                                   sp_contact=contact, comments=comments)
    sales_prospect.save()
    return sales_prospect


def update_sales_prospect_helper(request, sp, address, contact):
    sp.first_name = request.POST.get('first_name')
    sp.middle_initial = request.POST.get('middle_initial')
    sp.last_name = request.POST.get('last_name')
    sp.sales_type = request.POST.get('sales_type')
    sp.sales_probability = request.POST.get('sales_probability')
    sp.comments = request.POST.get('comments')

    #Logic section
    if address is not None:
        sp.sp_address = address
    if contact is not None:
        sp.sp_contact = contact

    sp.sp_business_name = request.POST.get('sp_business_name')
    if sp.sp_business_name == '' or sp.sp_business_name is None:
        sp.sp_business_name = None

    sp.is_business = boolean_helper(request.POST.get('is_business'))

    try:
        sp.sp_liberty_contact = Employee.objects.get(pk=request.POST.get('sp_liberty_contact'))
    except ValueError:
        sp.sp_liberty_contact = None

    sp.is_client = boolean_helper(request.POST.get('is_client'))

    sp.save(update_fields=['first_name', 'middle_initial',
                           'last_name', 'sp_liberty_contact',
                           'sp_business_name', 'is_business',
                           'sales_type', 'sales_probability',
                           'initial_contact_date', 'sp_address',
                           'sp_contact', 'comments'])
    sp.save()
    return sp
    #TODO -- Add is_client == True support
    if sp.is_client:
        pass
        #convert to Client


def sales_prospect_to_client_helper(sales_prospect):
    pass


    #endregion