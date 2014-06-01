from django.core.context_processors import request
from django.shortcuts import render, get_object_or_404, get_list_or_404, render_to_response
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse, HttpResponseRedirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from django.contrib.auth.models import User
from django.template import RequestContext
from Common.models import Address, Billing, Card, CallList, Genre, Contact, UserProfile
from Common.forms import AddressForm, CardForm, BillingForm, CallListForm, ContactForm, \
    CallListContactForm, UserProfileForm, UserForm
from helpermethods import form_generator, dict_generator, create_billing_helper, validation_helper, \
    create_address_helper, create_card_helper, update_address_helper, update_billing_helper, \
    update_card_helper, create_contact_helper, create_call_list_helper, create_calllist_contact_helper, \
    update_call_list_helper, update_calllist_contact
from Client.models import Client
from Client.helpermethods import update_client_billing_helper
from Site.models import Site

#region globals
add_client_billing = 'client/addclientbilling.html'

#endregion

#region BillingViews


def addclientbilling(request, pk):
    """
    View to add Client Billing.
    @param request: request.
    @param pk: Client pk.
    @return: Http.
    """
    template_name = 'client/addclientbilling.html'
    form_list = form_generator(3)
    client = Client.objects.get(client_id=pk)

    if request.method == 'POST':
        form_list[0] = BillingForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = CardForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address = create_address_helper(form_list[1])
            card = create_card_helper(request)
            billing = create_billing_helper(request, address=address, card=card)
            client_updated = update_client_billing_helper(client, billing)
            return HttpResponseRedirect(reverse('Client:details',
                                                kwargs={'pk': client_updated.client_id}))
        else:
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = BillingForm()
        form_list[1] = AddressForm()
        form_list[2] = CardForm()
        return render(request, template_name, dict_generator(form_list))


def editclientbilling(request, pk):
    form_list = form_generator(3)
    template_name = 'client/editclientbilling.html'
    client = Client.objects.get(client_billing_id=pk)

    # Dictionaries
    billing = Billing.objects.get(pk=pk)
    address = Address.objects.get(pk=billing.billing_address_id)
    card = Card.objects.get(pk=billing.card_id)

    address_dict = {
        'street': address.street, 'unit': address.unit, 'city': address.city,
        'state': address.state, 'zip_code': address.zip_code
    }
    billing_dict = {
        'profile_name': billing.profile_name, 'method': billing.method
    }
    card_dict = {
        'card_number': card.card_number, 'card_code': card.card_code,
        'card_type': card.card_type, 'card_expiration': card.card_expiration
    }

    if request.method == 'POST':
        form_list[0] = BillingForm(request.POST)
        form_list[1] = AddressForm(request.POST)
        form_list[2] = CardForm(request.POST)

        validation = validation_helper(form_list)
        if validation:
            address_up = update_address_helper(request, address)
            card_up = update_card_helper(request, card)
            billing_up = update_billing_helper(request, billing, address_up, card_up)
            return HttpResponseRedirect(reverse('Client:details',
                                                kwargs={'pk': client.client_id}))
        else:
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = BillingForm(billing_dict)
        form_list[1] = AddressForm(address_dict)
        form_list[2] = CardForm(card_dict)
        return render(request, template_name, dict_generator(form_list))

#endregion

#region CallList


class CallListDetails(DetailView):
    model = CallList
    call_list_id = 'pk'
    context_object_name = 'calllist_detail'
    template_name = 'client/calllistdetails.html'

    def get_context_data(self, **kwargs):
        context = super(CallListDetails, self).get_context_data(**kwargs)
        calllist = self.get_object()
        context['contact_detail'] = Contact.objects.get(pk=calllist.cl_contact_id)
        context['site'] = Site.objects.get(site_call_list=calllist.call_list_id)
        return context


def addcalllist(request, pk):
    template_name = 'client/addclientcalllist.html'
    site = Site.objects.get(pk=pk)
    form_list = form_generator(2)

    if request.method == 'POST':
        form_list[0] = CallListForm(request.POST)
        form_list[1] = CallListContactForm(request.POST)
        if validation_helper(form_list):
            contact = create_calllist_contact_helper(request)
            call_list = create_call_list_helper(form_list[0], contact, site)
            # Assumption a site must have a client
            related_client = Client.objects.get(pk=site.site_client_id)
            return HttpResponseRedirect(reverse('Client:details',
                                                kwargs={'pk': related_client.client_id}))
        else:
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = CallListForm()
        form_list[1] = CallListContactForm()
        fd = dict_generator(form_list)
        fd['site'] = site
        return render(request, template_name, fd)


def updatecalllist(request, pk):
    template_name = 'client/editclientcalllist.html'
    form_list = form_generator(2)
    calllist = CallList.objects.get(pk=pk)
    contact = Contact.objects.get(pk=calllist.cl_contact_id)
    site = Site.objects.get(site_call_list=calllist.call_list_id)

    contact_dict = {
        'phone': contact.phone, 'phone_extension': contact.phone_extension
    }
    calllist_dict = {
        'first_name': calllist.first_name, 'middle_initial': calllist.middle_initial,
        'last_name': calllist.last_name, 'cl_order': calllist.cl_order,
        'cl_is_enabled': calllist.cl_is_enabled, 'cl_genre': calllist.cl_genre_id
    }

    if request.method == 'POST':
        form_list[0] = CallListContactForm(request.POST)
        form_list[1] = ContactForm(request.POST)

        if validation_helper(form_list):
            contact_up = update_calllist_contact(request, contact)
            calllist_up = update_call_list_helper(request, calllist, contact_up)
            return HttpResponseRedirect(reverse('Client:sitedetails',
                                                kwargs={'pk': site.site_id}))
        else:
            return render(request, template_name, dict_generator(form_list))
    else:
        form_list[0] = CallListForm(calllist_dict)
        form_list[1] = CallListContactForm(contact_dict)
        return render(request, template_name, dict_generator(form_list))

#endregion

#region Signup

def register(request):
    # Request's context
    context = RequestContext(request)
    template_name = 'common/register.html',

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render_to_response(
            template_name,
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered},
            context)

#endregion

#region Login



#endregion