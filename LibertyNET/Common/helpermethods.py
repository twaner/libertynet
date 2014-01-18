from models import Address, Contact, Card, Billing
from Client.models import Client

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
    address = Address.objects.create(street=street, unit=unit, city=city, state=state, zip_code=zip_code)
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
    office = request.POST.get('office_phone')
    office_ext = request.POST.get('office_phone_extension')
    contact = Contact.objects.create(phone=phone, cell=cell, office_phone=office,
                                     office_phone_extension=office_ext,
                                     email=email, work_email=work_email,
    )
    return contact


def create_contact_helper(request):
    """
    Creates employee based contact object based on request info.
    @param request: request.
    @return: contact object.
    """
    phone = request.POST.get('phone')
    phone_extension = request.POST.get('phone_extension')
    cell = request.POST.get('cell')
    email = request.POST.get('email')
    work_email = request.POST.get('work_email')
    office = request.POST.get('office_phone')
    office_ext = request.POST.get('office_phone_extension')
    website = request.POST.get('website')
    contact = Contact.objects.create_contact(phone=phone, phone_extension=phone_extension,
                                             cell=cell, office_phone=office,
                                             office_phone_extension=office_ext,
                                             email=email, work_email=work_email,
                                             website=website)
    return contact

#endregion

#region Billing Helper Methods


def create_billing_helper(request):
    profile_name = request.POST.get('profile_name')
    method = request.POST.get('method')
    billing_address = request.POST.get('billing_address')
    card = request.POST.get('card')

    billing = Billing.objects.create(profile_name=profile_name,
                                     method=method, billing_address=billing_address, card=card)
    billing.save()
    return billing


#endregion

#region Card Helper Methods


def create_card_helper(request):
    first_name = request.POST.get('first_name')
    middle_initial = request.POST.get('middle_initial')
    last_name = request.POST.get('last_name')
    card_number = request.POST.get('card_number')
    card_code = request.POST.get('card_code')
    card_type = request.POST.get('card_type')

    card = Card.objects.create(first_name=first_name, middle_initial=middle_initial, last_name=last_name,
                               card_number=card_number, card_code=card_code, card_type=card_type)
    card.save()
    return card


#endregion

#region Form Helpers


def validation_helper(form_list):
    """
    Handles a list of request and runs is_valid() on them.
    @param form_list: list of forms.
    @return: Boolean based on validation.
    """
    for i in form_list:
        if not i.is_valid():
            return False
        else:
            return True
    """
    q = [False if not i.is_valid() else True for i in form_list]
    """


def form_generator(n):
    """
    Dynamically generates a list to of items called 'form + i'.
    @param n: number of elements to add to the list.
    @return: list with n elements.
    """
    form_list = []
    [form_list.append("form" + str(i)) for i in range(n)]
    return form_list


def form_errors_printer(form_list):
    q = 0
    for i in form_list:
        if not i.is_valid():
            print("Form[", q, "] not valid =>", i.errors)
        q += 1


def dict_generator(form_list):
    """
    genrates dictionary to hold forms.
    @param form_list: List of forms.
    @type form_list: List
    @param: list.
    @return: dictionary with k, v for forms.
    """
    d = {}
    [d.update({"form" + str(i): form_list[i]}) for i in range(len(form_list))]
    return d


def form_worker(form_list, requested, *args):
    """
    Takes form list and either runs a request.POST or generate unbound forms.
    @param requested: Boolean for whether to run request routine
    @param form_list: form list.
    @param args: ModelForms
    @return:
    """
    if requested:
        for i in range(len(form_list)):
            form_list[i] = args[i](request.POST)
    else:
        for i in range(len(form_list)):
            form_list[i] = args[i]

    return form_list


def boolean_helper(*args):
    """
    Takes boolean from form and handles string passed
    @param args: boolean field from form
    @return: boolean updated to reflect selection
    """
    worker = True
    print('before if boolean', args[0])
    if args[0] is None or args[0] == 'None':
        worker = False
    return worker
    #endregion