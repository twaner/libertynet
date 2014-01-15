from models import Address, Contact

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
    contact = Contact.objects.create(phone=phone, cell=cell, email=email, work_email=work_email)
    return contact

#endregion

#region Form Helpers


def validation_helper(form_list):
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


def dict_generator(form_list):
    """
    genrates dictionary to hold forms.
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

#endregion