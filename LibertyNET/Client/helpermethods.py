from models import Client, Sales_Prospect
from Common.models import Address, Billing, Contact
from Common.helpermethods import boolean_helper

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
    client_address = [i for i in args if type(i) == Address]
    client_contact = [q for q in args if type(q) == Contact]

    client = Client.objects.create(first_name=first_name, middle_initial=middle_initial,
                                   last_name=last_name, client_number=client_number,
                                   business_name=business_name, is_business=is_business,
                                   client_address=args[0], client_contact=args[1],
                                   client_date=client_date)
    return client

    #endregion