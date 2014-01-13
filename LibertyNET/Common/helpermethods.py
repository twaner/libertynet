from models import Address, Contact,

#region Address Helpers


def create_address_helper(request):
    """
    creates an address object based on request data.
    @param request: request data.
    @return: address object.
    """
    street = request.POST.get('street')
    unit = request.POST.get('unit')
    city = request.POST.get('city')
    state = request.POST.get('state')
    zip_code = request.POST.get('zip_code')

    address = Address.objects.create_address(street, unit, city, state, zip_code)
    return address


#endregion

#region Contact Helpers


def create_employee_contact_helper(request):
    """
    Creates employee based contact object based on request info.
    @param request: request.
    @return: contact object.
    """
    phone = request.POST.get('phone')
    cell = request.POST.get('cell')
    email = request.POST.get('email')
    work_email = request.POST.get('work_email')
    contact = Contact.objects.create_employee_contact(phone, cell, email, work_email)
    return contact

#endregion