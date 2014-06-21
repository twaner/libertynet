from models import Address, Contact, Card, Billing, CallList, Genre
from django.db import models
import django.forms
from datetime import datetime, timedelta, date
from django.shortcuts import redirect, HttpResponseRedirect
from django.core.urlresolvers import reverse
import types

#region Address Helpers


def create_address_helper(form):
    """
    creates an address object based on request data.
    @param request: request data.
    @return: address object.
    """
    street = form.cleaned_data['street']
    unit = form.cleaned_data['unit']
    city = form.cleaned_data['city']
    state = form.cleaned_data['state']
    zip_code = form.cleaned_data['zip_code']
    address = Address.objects.create_address(street=street, unit=unit, city=city, state=state, zip_code=zip_code)
    return address


def update_address_helper(form, address):
    """
    Updates an address object.
    @param form: form.
    @param address: address object.
    @return: address.
    """
    address.street = form.cleaned_data['street']
    address.unit = form.cleaned_data['unit']
    address.city = form.cleaned_data['city']
    address.state = form.cleaned_data['state']
    address.zip_code = form.cleaned_data['zip_code']
    address.save(update_fields=['street', 'unit', 'city', 'state', 'zip_code'])
    return address


#endregion

#region Contact Helpers


def create_employee_contact_helper(form):
    """
    Creates employee based contact object based on request info.
    @param form: request.
    @return: contact object.
    """
    phone = form.cleaned_data['phone']
    cell = form.cleaned_data['cell']
    email = form.cleaned_data['email']
    work_email = form.cleaned_data['work_email']
    office = form.cleaned_data['office_phone']
    office_ext = form.cleaned_data['office_phone_extension']
    contact = Contact.objects.create(phone=phone, cell=cell, office_phone=office,
                                     office_phone_extension=office_ext,
                                     email=email, work_email=work_email)
    return contact


def update_contact_employee_helper(form, contact):
    """
    Updates a contact object for an Employee.
    @param request: request.
    @param contact: Contact object.
    @return: Contact object.
    """
    contact.phone = form.cleaned_data['phone']
    contact.cell = form.cleaned_data['cell']
    contact.email = form.cleaned_data['email']
    contact.work_email = form.cleaned_data['work_email']
    contact.office_phone = form.cleaned_data['office_phone']
    contact.office_phone_extension = form.cleaned_data['office_phone_extension']
    contact.save(update_fields=['phone', 'cell', 'office_phone',
                                'office_phone_extension', 'email', 'work_email'])
    return contact


def create_contact_helper(form):
    """
    Creates employee based contact object based on request info.
    @param request: request.
    @return: contact object.
    """
    phone = form.cleaned_data['phone']
    phone_extension = form.cleaned_data['phone_extension']
    cell = form.cleaned_data['cell']
    email = form.cleaned_data['email']
    work_email = form.cleaned_data['work_email']
    office = form.cleaned_data['office_phone']
    office_ext = form.cleaned_data['office_phone_extension']
    website = form.cleaned_data['website']
    contact = Contact.objects.create(phone=phone, phone_extension=phone_extension,
                                     cell=cell, office_phone=office,
                                     office_phone_extension=office_ext,
                                     email=email, work_email=work_email,
                                     website=website)
    contact.save()
    return contact


def create_contact_client_calllog_helper(form):
    """
    Creates employee based contact object based on request info.
    @param request: request.
    @return: contact object.
    """
    phone = form.cleaned_data['phone']
    phone_extension = form.cleaned_data['phone_extension']
    office = form.cleaned_data['office_phone']
    office_ext = form.cleaned_data['office_phone_extension']
    contact = Contact.objects.create(phone=phone, phone_extension=phone_extension,
                                     office_phone=office, office_phone_extension=office_ext)
    contact.save()
    return contact


def updated_contact_helper(form, contact):
    """
    Updates a contact object.
    @param request: request.
    @param contact: Contact object.
    @return: Contact object.
    """
    contact.phone = form.cleaned_data['phone']
    contact.phone_extension = form.cleaned_data['phone_extension']
    contact.cell = form.cleaned_data['cell']
    contact.email = form.cleaned_data['email']
    contact.work_email = form.cleaned_data['work_email']
    contact.office = form.cleaned_data['office_phone']
    contact.office_ext = form.cleaned_data['office_phone_extension']
    contact.website = form.cleaned_data['website']
    contact.save(update_fields=['phone', 'phone_extension', 'cell', 'office_phone'
                                                                    'office_phone_extension', 'website' 'email',
                                'work_email'])
    return contact


def update_contact_helper(form, contact):
    """
    Updates a full contact object.
    @param form: request.
    @param contact: Contact object.
    @return: Contact.
    """
    contact.phone = form.cleaned_data['phone']
    contact.phone_extension = form.cleaned_data['phone_extension']
    contact.cell = form.cleaned_data['cell']
    contact.email = form.cleaned_data['email']
    contact.work_email = form.cleaned_data['work_email']
    contact.website = form.cleaned_data['website']
    contact.office_phone = form.cleaned_data['office_phone']
    contact.office_phone_extension = form.cleaned_data['office_phone_extension']
    contact.save(update_fields=['phone', 'phone_extension', 'cell', 'office_phone',
                                'office_phone_extension', 'email', 'work_email', 'website'])
    return contact


def create_calllist_contact_helper(form):
    phone = form.cleaned_data['phone']
    phone_extension = form.cleaned_data['phone_extension']

    contact = Contact.objects.create(phone=phone, phone_extension=phone_extension)
    contact.save()
    return contact


def update_calllist_contact(form, contact):
    contact.phone = form.cleaned_data['phone']
    contact.phone_extension = form.cleaned_data['phone_extension']

    contact.save(update_fields=['phone', 'phone_extension'])
    return contact


#endregion

#region Billing Helper Methods


def create_billing_helper(form, address, card):
    """
    Creates a new Billing object.
    @param address: Address object.
    @param card: Card object.
    @param request: request.
    @return: Billing.
    """
    profile_name = form.cleaned_data['profile_name']
    method = form.cleaned_data['method']
    billing_address = address
    card = card

    billing = Billing.objects.create(profile_name=profile_name,
                                     method=method, billing_address=billing_address, card=card)
    billing.save()
    return billing


def update_billing_helper(form, billing, address, card):
    billing.profile_name = form.cleaned_data['profile_name']
    billing.method = form.cleaned_data['method']
    billing.billing_address = address
    billing.card = card

    billing.save(update_fields=['profile_name',
                                'method', 'billing_address', 'card'])
    return billing


#endregion

#region CallList


def create_call_list_helper(form, contact, site):
    """
    Creates a Call List.
    @param form: request.
    @param contact: Contact.
    @return: Call List.
    """
    first_name = form.cleaned_data['first_name']
    middle_initial = form.cleaned_data['middle_initial']
    last_name = form.cleaned_data['last_name']
    cl_contact = contact
    cl_order = form.cleaned_data['cl_order']
    cl_is_enabled = boolean_helper(form.cleaned_data['cl_is_enabled'])
    cl_genre = Genre.objects.get(pk=form.cleaned_data['cl_genre'].genre_id)

    call_list = CallList.objects.create_call_list(first_name=first_name, last_name=last_name,
                                                  middle_initial=middle_initial, cl_contact=cl_contact,
                                                  cl_order=cl_order, cl_is_enabled=cl_is_enabled,
                                                  cl_genre=cl_genre)
    call_list.save()
    # Add to site
    site.site_call_list.add(call_list)
    return call_list


def create_call_list_helper_not_site(form, contact):
    """
    Creates a Call List and does NOT add it to a Site.
    @param form: request.
    @param contact: Contact.
    @return: Call List.
    """
    first_name = form.cleaned_data['first_name']
    middle_initial = form.cleaned_data['middle_initial']
    last_name = form.cleaned_data['last_name']
    cl_contact = contact
    cl_order = form.cleaned_data['cl_order']
    cl_is_enabled = boolean_helper(form.cleaned_data['cl_is_enabled'])
    cl_genre = Genre.objects.get(pk=form.cleaned_data['cl_genre'].genre_id)

    call_list = CallList.objects.create_call_list(first_name=first_name, last_name=last_name,
                                                  middle_initial=middle_initial, cl_contact=cl_contact,
                                                  cl_order=cl_order, cl_is_enabled=cl_is_enabled,
                                                  cl_genre=cl_genre)
    call_list.save()
    return call_list



def update_call_list_helper(form, calllist, contact):
    """
    Updates a Call List
    @param request: request.
    @param calllist: Call List.
    @param contact: Contact.
    @return: Call List.
    """
    calllist.first_name = form.cleaned_data['first_name']
    calllist.middle_initial = form.cleaned_data['middle_initial']
    calllist.last_name = form.cleaned_data['last_name']
    calllist.cl_contact = contact
    calllist.cl_order = form.cleaned_data['cl_order']
    calllist.cl_is_enabled = boolean_helper(form.cleaned_data['cl_is_enabled'])
    calllist.cl_genre = Genre.objects.get(pk=form.cleaned_data['cl_genre'])

    calllist.save(update_fields=['first_name', 'last_name',
                                 'middle_initial', 'cl_contact',
                                 'cl_order', 'cl_is_enabled',
                                 'cl_genre'])
    calllist.save()
    return calllist


#endregion

#region Card Helper Methods


def create_card_helper(form):
    """
    Creates a Credit Card.
    @param request: request.
    @return: Credit Card.
    """
    first_name = form.cleaned_data['first_name']
    middle_initial = form.cleaned_data['middle_initial']
    last_name = form.cleaned_data['last_name']
    card_number = form.cleaned_data['card_number']
    card_code = form.cleaned_data['card_code']
    card_type = form.cleaned_data['card_type']
    card_expiration = form.cleaned_data['card_expiration']

    card = Card.objects.create(first_name=first_name, middle_initial=middle_initial, last_name=last_name,
                               card_number=card_number, card_code=card_code, card_type=card_type,
                               card_expiration=card_expiration)
    card.save()
    return card


def update_card_helper(form, card):
    """
    Updates a Credit Card.
    @param form: request.
    @param card: Card.
    @return: Card
    """
    card.first_name = form.cleaned_data['first_name']
    card.middle_initial = form.cleaned_data['middle_initial']
    card.last_name = form.cleaned_data['last_name']
    card.card_number = form.cleaned_data['card_number']
    card.card_code = form.cleaned_data['card_code']
    card.card_type = form.cleaned_data['card_type']
    card.card_expiration = form.cleaned_data['card_expiration']

    card.save(update_fields=['first_name', 'middle_initial', 'last_name',
                             'card_number', 'card_code', 'card_type',
                             'card_expiration'])
    assert isinstance(card, Card)
    return card


#endregion

#region General Helpers


def get_model_fields(model):
    return model._meta.fields


def validation_helper(form_list):
    """
    Handles a list of request and runs is_valid() on them.
    @param form_list: list of forms.
    @return: Boolean based on validation.
    """
    invalid = 0
    if type(form_list) is not list:
        form_list = [form_list]
    for i in form_list:
        if not i.is_valid():
            invalid += 1
            print('VALIDATION_HELPER ==> Errors: %s | Num Errors: %s \n Form: %s ' % (i.errors, len(i.errors), type(i)))
            # for q in i:
            #     print('validation_helper: %s' % q.name_of_field.errors)
        else:
            i.is_valid()
            print('VALIDATION_HELPER ==> %s ' % i.is_valid())
    print('VALIDATION_HELPER invalid=%s' % invalid)
    if invalid >= 1:
        return False
    else:
        return True


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
    if isinstance(form_list, list):
        for i in form_list:
            if not i.is_valid():
                print("Form[", q, "] not valid =>", i.errors)
            q += 1
    else:
        print(form_list.errors)


def dict_generator(form_list):
    """
    generates dictionary to hold forms.
    @param form_list: List of forms.
    @type form_list: List
    @param: list.
    @return: dictionary with k, v for forms.
    """
    d = {}
    [d.update({"form" + str(i): form_list[i]}) for i in range(len(form_list))]
    return d


def form_worker(form_list, request, *args):
    """
    Takes form list and either runs a request.POST or generate unbound forms.
    @param request: Boolean for whether to run request routine
    @param form_list: form list.
    @param args: ModelForms
    @return:
    """
    if request:
        for i in range(len(form_list)):
            form_list[i] = args[i](request.POST)
    else:
        for i in range(len(form_list)):
            form_list[i] = args[i]

    return form_list


def readonly_worker(form, field_list):
    for i in field_list:
        if isinstance(form.fields[i].widget, django.forms.widgets.Select) or \
                isinstance(form.fields[i], django.forms.models.ModelChoiceField):
            form.fields[i].widget.attrs['readonly'] = True
        else:
            form.fields[i].widget.attrs['readonly'] = True


def boolean_helper(*args):
    """
    Takes boolean from form and handles string passed
    @param args: boolean field from form
    @return: boolean updated to reflect selection
    """
    worker = True
    print('before boolean_helper', args[0])
    if not args[0]:
        worker = False
    elif args[0] is None or args[0] == 'None' or args[0] == '':
        worker = False
    print('After boolean_helper', worker)
    return worker


def get_function_name(func):
    """
    Gets a functions name as string.
    @param func: function.
    @return: function name as string.
    """
    return func.__name__.upper()


#region Date and Time Helpers

def time_str_to_time(time_str):
    """
    Converts a string representation of time into a datetime.time object.
    @param time_str: Times as a string.
    @return: formatted datetime.time.
    """
    fmt ='%H:%M'
    return datetime.strptime(time_str, fmt).time()


def time_worker(time1):
    """
    Takes a type datetime.time object and creates a datetime.timedelta object.
    Checks if time1 is a string and changes to datetime.time if it is.
    @param time1: time.
    @return: datetime.timedelta of time1.
    """
    if isinstance(time1, str):
        time1 = time_str_to_time(time1)
    return timedelta(hours=time1.hour, minutes=time1.minute)


def seconds_to_hours(time_obj):
    """
    Takes a datetime.timedelta object and divides by 3600 (seconds * minutes)
    to get hours worked as float.
    @param time_obj: datetime.timedelta of time worked.
    @return: Hours worked.
    """
    return float(time_obj.seconds) / 3600


def time_diff(start, end):
    """
    Gets difference of two
    @param start:
    @param end:
    @return:
    """
    if start and end:
        return time_worker(end) - time_worker(start)
    else:
        return timedelta(hours=0, minutes=0)


def time_delta_to_str(td):
        return ':'.join(str(timedelta(hours=td)).split(':')[:2])


def date_change(num):
    """
    Adds num to today's Date.
    @param num: number of days to add.
    @return: future date.
    """
    return (date.today() + timedelta(days=num)).strftime("%Y-%m-%d")

#region Assert Helpers


def assert_equals_worker(self, expected, got):
    """
    Performs an assert and gives clean message on failure.
    @param s: Self.
    @param expected: Expected value.
    @param got: Received value.
    @return:
    """
    return self.assertEquals(got, expected,
                             '%s not equal. Expected %s got %s' %
                             (str(got), expected, got))


def assert_equals_worker_long(self, expected, got, name):
    """
    Performs an assert and gives clean message on failure.
    @param self: Self.
    @param expected: Expected value.
    @param got: Received value.
    @return:
    """
    return self.assertEquals(got, expected,
                             '%s %s not equal. Expected %s got %s' %
                             (name.upper(), str(got), expected, got))


def assert_true_non_instance_worker(self, got):
    return self.assertTrue(got, '%s is not True' % str(got).upper())


def assert_false_non_instance_worker(self, got):
    return self.assertFalse(got, '%s is not False' % str(got).upper())


def assert_true_worker(self, exp, got):
    """
    Performs an assert and gives clean message on failure.
    @param self: Self.
    @param exp: Expected value.
    @param got: Received value.
    @return:
    """
    return self.assertTrue(isinstance(got, exp), '%s is not %s' % (str(got), str(exp)))


def assert_in_worker(self, expected, got):
    return self.assertIn(expected, got, '%s is not in %s' % (expected, str(got)))


def form_assert_true_worker(self, form):
    """
    Runs assertTrue on a Form. Prints formatted message on failure.
    @param self: Self.
    @param form: Form object.
    @return: assertTrue.
    """
    return self.assertTrue(form.is_valid(), "%s is not valid" % form.__class__.__name__)


def form_assert_false_worker(self, form):
    """
    Runs assertTrue on a Form. Prints formatted message on failure.
    @param self: Self.
    @param form: Form object.
    @return: assertTrue.
    """
    return self.assertFalse(form.is_valid(), "%s is valid" % form.__class__.__name__)


def model_to_dict(instance):
    data = {}
    for field in instance._meta.fields:
        data[field.name] = field.value_from_object(instance)
        if isinstance(field, models.ForeignKey):
            data[field.name] = field.rel.to.objects.get(pk=data[field.name])
    return data

#endregion

#region Auth


def show_login():
    pass
    #return HttpResponseRedirect(reverse('Common:login'))

#endregion