from models import Client, Sales_Prospect
from Common.models import Address, Billing, Contact

#region Client


def create_client_helper(request, *args):
    """
    Takes a request, and FK objects and creates a new client.
    @param request: request.
    @param args: Address, Co
    @return:
    """
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    middle_initial = request.POST.get('middle_initial')
    client_number = request.POST.get('client_number')
    business_name = request.POST.get('business_name')
    is_business = request.POST.get('is_business')
    client_date = request.POST.get('client_date')

    # Handle args
    for i in range(len(args)):
        if args[i] == Address:
            client_address = args[i]
        elif args[i] == Contact:
            client_contact = args[i]
        elif args[i] == Billing:
            client_billing = args[i]

    client = Client.objects.create(first_name=first_name, middle_initial=middle_initial,
                                   last_name=last_name, client_number=client_number,
                                   business_name=business_name, is_business=is_business,
                                   client_address=client_address, client_contact=client_contact,
                                   client_billing=client_billing, client_date=client_date)
    return client

    #endregion