from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from Common.models import Person, CallLog
from datetime import date


#region ModelManagers


class ClientManager(models.Manager):
    def create_client(self, first_name, middle_initial, last_name, client_number, business_name,
                      is_business, client_address,
                      client_contact, client_date):
        """
        Base create for a client with business attributes.
        @param first_name: client's first name.
        @param middle_initial: client's middle initial.
        @param last_name: client's last name.
        @param client_number: the client's number.
        @param business_name: business name if business.
        @param is_business: is client a business.
        @param client_address: client's address.
        @param client_contact: client's contact info.
        @param client_date: date client opened account with company.
        @return: client object
        """
        client = self.create(first_name=first_name, middle_initial=middle_initial.upper(), last_name=last_name,
                             client_number=client_number, business_name=business_name,
                             is_business=is_business, client_address=client_address,
                             client_contact=client_contact, client_date=client_date)
        client.save()
        return client

    def create_client(self, first_name, middle_initial, last_name, client_number,
                      client_address, client_contact, client_date):
        """
        Base create for a client with NO business attributes
        @param first_name: client's first name.
        @param middle_initial: client's middle initial.
        @param last_name: client's last name.
        @param client_number: the client's number.
        @param client_address: client's address.
        @param client_contact: client's contact info.
        @param client_date: date client opened account with company.
        @return: client object
        """
        client = self.create(first_name=first_name, middle_initial=middle_initial.upper(), last_name=last_name,
                             client_number=client_number, client_address=client_address,
                             client_contact=client_contact, client_date=client_date)
        client.save()
        return client

    def _get_residential(self):
        """
        Model manager for filtering residential clients.
        @return: queryset of residential accounts.
        """
        return self.get_query_set().filter(is_business='0')

    def _get_commercial(self):
        """
        Model manager for filtering commercial clients.
        @return: queryset of commercial accounts.
        """
        return self.get_queryset().filter(is_business='1')

    residential = property(_get_residential)
    commercial = property(_get_commercial)


class BusinessManager(models.Manager):
    def get_query_set(self):
        """
        Model manager for commercial accounts.
        Filters clients on is_business boolean.
        @return: query set of commercial accounts.
        """
        return super(BusinessManager, self).get_query_set().filter(is_business='1')


class PersonalManager(models.Manager):
    def get_query_set(self):
        """
        Model manager for residential accounts.
        Filters clients on is_business boolean.
        @return: query set of residential accounts.
        """
        return super(PersonalManager, self).get_query_set().filter(is_business='0')


class SalesProspectManager(models.Manager):
    def create_sales_prospect(self, first_name, middle_initial, last_name, sp_business_name,
                              is_business, sp_liberty_contact, sales_type, sales_probability,
                              initial_contact_date, comments, sp_address, sp_contact, is_client):
        """
        Creates and returns a sales prospect.
        @param first_name: sales prospect's first name.
        @param middle_initial: sales prospect's middle initial.
        @param last_name: sales prospect's last name.
        @param sp_business_name: sales prospect's business name (can be null)
        @param is_business: sales prospect is commercial accounts.
        @param is_client: Is sales prospect a client.
        @param sp_liberty_contact: liberty employee who brought contact.
        @param sales_type: type of sale.
        @param sales_probability: estimate of sale's probability.
        @param initial_contact_date: contact date.
        @param comments: comments.
        @param sp_address: sales prospect's address (optional)
        @param sp_contact: sales prospect's contact info.
        @return: Sales Prospect.
        """
        sales_prospect = self.create(first_name=first_name, middle_initial=middle_initial.upper(), last_name=last_name,
                                     sp_business_name=sp_business_name, is_business=is_business,
                                     sp_liberty_contact=sp_liberty_contact,
                                     sales_type=sales_type, initial_contact_date=initial_contact_date,
                                     comments=comments, sp_address=sp_address, is_client=is_client,
                                     sales_probability=sales_probability,
                                     sp_contact=sp_contact)
        sales_prospect.save()
        return sales_prospect

    def create_sales_prospect(self, first_name, middle_initial, last_name,
                              sp_liberty_contact, sales_type, sales_probability,
                              initial_contact_date, comments, sp_address, sp_contact):
        """
        Creates and returns a sales prospect with NO business attributes.
        @param first_name: sales prospect's first name.
        @param middle_initial: sales prospect's middle initial.
        @param last_name: sales prospect's last name.
        @param sp_liberty_contact: liberty employee who brought contact.
        @param sales_type: type of sale.
        @param sales_probability: estimate of sale's probability.
        @param initial_contact_date: contact date.
        @param comments: comments.
        @param sp_address: sales prospect's address (optional)
        @param sp_contact: sales prospect's contact info.
        @return: Sales Prospect.
        """
        sales_prospect = self.create(first_name=first_name, middle_initial=middle_initial.upper(), last_name=last_name,
                                     sp_liberty_contact=sp_liberty_contact,
                                     sales_type=sales_type, initial_contact_date=initial_contact_date,
                                     comments=comments, sp_address=sp_address,
                                     sales_probability=sales_probability,
                                     sp_contact=sp_contact)
        sales_prospect.save()
        return sales_prospect


class ClientCallLogManager(models.Manager):
    def create_client_calllog(self, client_id, caller, call_date, call_time, purpose, notes, next_contact):
        """
        Creates a ClientCallLog.
        @param client_id: Client Id.
        @param caller: Liberty Employee.
        @param call_date: Date of call.
        @param call_time: Time of call.
        @param purpose: Purpose of call.
        @param notes: Notes on call.
        @param next_contact: Next date to contact.
        @return: ClientCallLog.
        """
        calllog = self.create(client_id=client_id, caller=caller, call_date=call_date, call_time=call_time,
                              purpose=purpose, notes=notes, next_contact=next_contact)
        calllog.save()
        return calllog

    def get_next_contact_date(self, client):
        """
        Gets the next time a call should be made.
        @param client: Client.
        @return: ClientCallLog that has date of next call.
        """
        #call = ClientCallLog.objects.filter(client_id=client).latest('next_contact')
        call = ClientCallLog.objects.filter(client_id=client).\
            filter(next_contact__gte=date.today().strftime("%Y-%m-%d")).first()
        return call


class SalesProspectCallLogManager(models.Manager):
    def create_sales_calllog(self, sales_id, caller, call_date, call_time, purpose, notes, next_contact):
        """
        Creates a SalesProspectCallLog.
        @param sales_id: SalesProspect Id.
        @param caller: Liberty Employee.
        @param call_date: Date of call.
        @param call_time: Time of call.
        @param purpose: Purpose of call.
        @param notes: Notes on call.
        @param next_contact: Next date to contact.
        @return: SalesProspectCallLog.
        """
        calllog = self.create(sales_id=sales_id, caller=caller, call_date=call_date, call_time=call_time,
                              purpose=purpose, notes=notes, next_contact=next_contact)
        calllog.save()
        return calllog

    def get_next_contact_date(self, sales):
        """
        Gets the CallList with the soonest contact date.
        @param sales: SalesProspect.
        @return: SalesProspectCallLog with date of soonest contact.
        """
        call = SalesProspectCallLog.objects.filter(sales_id=sales).\
            filter(next_contact__gte=date.today().strftime("%Y-%m-%d")).first()
        return call

#endregion

#region Client Models


class Client(Person):

    """
    Client object. An object that contains attributes that a LS Client would have.
    """
    client_id = models.AutoField(primary_key=True)
    client_number = models.IntegerField(max_length=10)
    business_name = models.CharField(max_length=50, blank=True, null=True)
    is_business = models.BooleanField(default=False)
    client_address = models.ForeignKey('Common.Address')
    client_contact = models.ForeignKey('Common.Contact')
    client_billing = models.ForeignKey('Common.Billing', null=True, blank=True)
    client_date = models.DateField()

    objects = ClientManager()
    personal = PersonalManager()
    business = BusinessManager()

    def get_absolute_url(self):
        """
        Gets details view url.
        @return: details view url.
        """
        return reverse('Client:details', kwargs={'pk': self.client_id})

    def get_absolute_url_wrap(self):
        """
        Gets details view url.
        @return: details view url.
        """
        return reverse('Client:clientdetails_wrap', kwargs={'pk': self.client_id})

    def get_absolute_url_edit(self):
        """
        Gets edit view url.
        @return: edit view url.
        """
        return reverse('Client:editclient', kwargs={'pk': self.client_id})
        #@models.permalink
        #def get_absolute_url(self):
        #   return 'ClientDetailView', [str(self.client_id)] #{'pk': self.client_id}

    def get_absolute_url_edit_wrap(self):
        """
        Gets edit view url.
        @return: edit view url.
        """
        return reverse('Client:editclient_wrap', kwargs={'pk': self.client_id})

    def get_absolute_url_calllog(self):
        """
        Gets client call log view url.
        @return: client call log view url.
        """
        return reverse('Client:addclientcalllog', kwargs={'pk': self.client_id})

    def get_absolute_url_calllog_index(self):
        """
        Gets client call log index view url.
        @return: client call log index view url.
        """
        return reverse('Client:clientcalllogindex', kwargs={'pk': self.client_id})

    def clean(self):
        """
        Performs custom validation for creating a business Client.
        @raise ValidationError:
        """
        super(Client, self).clean()
        # Business validation
        if self.is_business and self.business_name == '':
            raise ValidationError('Please enter a business name')
        elif self.is_business is False and (self.business_name != ''):
            raise ValidationError("Please select 'Is Business'")

    def __str__(self):
        """
        Sets display for Client object to first and last name.
        @return: first and last name of Client.
        """
        if self.is_business:
            return self.business_name
        else:
            return '%s' % self.get_full_name()

    def is_a_business(self):
        """
            Checks if a client is a commercial account.
            @return: Business name or first name of the client.
            """
        if self.is_business:
            return True
        else:
            return False

    def get_full_name(self):
        if self.middle_initial != '':
            return u'%s %s %s' % (self.first_name, self.middle_initial, self.last_name)
        else:
            return u'%s %s' % (self.first_name, self.last_name)


#endregion

#region Sales Prospects


class SalesProspect(Person):
    """
    Sales Prospect model. 'sp' is used as abbreviation to save typing
    for FK fields.
    @field: sp_liberty_contact employee who got contact.
    """
    HIGH = 'H'
    MEDIUM = 'M'
    LOW = 'L'
    UNKNOWN = 'U'
    PROBABILITY = (
        (HIGH, 'High'),
        (MEDIUM, 'Medium'),
        (LOW, 'Low'),
        (UNKNOWN, 'Unknown'),
    )
    sales_prospect_id = models.AutoField(primary_key=True)
    sp_business_name = models.CharField(max_length=50, null=True, blank=True)
    is_business = models.BooleanField(default=False)
    sp_liberty_contact = models.ForeignKey('Employee.Employee', verbose_name="liberty employee", null=True, blank=True)
    sales_type = models.CharField(max_length=40, blank=True)
    sales_probability = models.CharField(choices=PROBABILITY, max_length=10)
    initial_contact_date = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=500, blank=True)
    sp_address = models.ForeignKey('Common.Address', verbose_name="prospect address", null=True, blank=True)
    sp_contact = models.ForeignKey('Common.Contact', verbose_name="prospect contact info", null=True, blank=True)
    is_client = models.BooleanField(default=False)

    objects = SalesProspectManager()

    def get_absolute_url(self):
        return reverse('Client:salesprospectdetails', kwargs={'pk': self.sales_prospect_id})

    def get_absolute_url_edit(self):
        return reverse('Client:editsalesprospect', kwargs={'pk': self.sales_prospect_id})

    def get_absolute_url_calllog(self):
        """
        Gets client call log view url.
        @return: client call log view url.
        """
        return reverse('Client:addsalescalllog', kwargs={'pk': self.sales_prospect_id})

    def get_absolute_url_calllog_index(self):
        """
        Gets client call log index view url.
        @return: client call log index view url.
        """
        return reverse('Client:salescalllogindex', kwargs={'pk': self.sales_prospect_id})

    def clean(self):
        super(SalesProspect, self).clean()
        # Business validation
        if self.is_business and self.sp_business_name == '':
            raise ValidationError('Please enter a business name')
        elif self.is_business is False and (self.sp_business_name != ''):
            raise ValidationError("Please select 'Is Business'")

    def __str__(self):
        """
        Sets display for Client object to first and last name.
        @return: first and last name of Client.
        """
        if self.is_business:
            return self.sp_business_name
        else:
            return u'%s %s %s' % (self.first_name, self.middle_initial, self.last_name)


#endregion

#region CallLogs


class ClientCallLog(CallLog):
    """
    CallLog object with fields for a Client.
    """
    id = models.AutoField(primary_key=True)
    client_id = models.ForeignKey('Client.Client')

    objects = ClientCallLogManager()

    def __str__(self):
        return 'Client: %s Call Date: %s' % (self.client_id, self.call_date)

    @property
    def full_details(self):
        """
        Gets client, call date and time.
        @return: client, call date and time.
        """
        return 'Client: %s Call Date: %s Time: %s' % (self.client_id, self.call_date, self.call_time)

    @property
    def complete_details(self):
        return 'Client: %s Purpose: %s Call Date: %s Time: %s' % (self.client_id, self.purpose,
                                                                  self.call_date, self.call_time)

    @property
    def next_call(self):
        """
        Gets next contact time for client.
        @return: next contact time for client.
        """
        return '%s' % self.next_contact

    def get_absolute_url(self):
        return reverse('Client:clientcalllogdetails', kwargs={'pk': self.id})

    def get_absolute_url_client(self):
        return reverse('Client:details', kwargs={'pk': self.client_id.client_id})

    def get_absolute_url_index(self):
        return reverse('Client:clientcalllogindex', kwargs={'pk': self.client_id.client_id})

    # TODO Create views
    # def get_absolute_url_edit(self):
    #     return reverse('Client:editclientcalllogdetails', kwargs={'pk': self.id})

class SalesProspectCallLog(CallLog):
    id = models.AutoField(primary_key=True)
    sales_id = models.ForeignKey('Client.SalesProspect')

    objects = SalesProspectCallLogManager()

    def __str__(self):
        return 'Prospect: %s Call Date: %s' % (self.sales_id, self.call_date)

    def get_absolute_url(self):
        return reverse('Client:salescalllogdetails', kwargs={'pk': self.id})

    def get_absolute_url_sales(self):
        return reverse('Client:salesprospectdetails', kwargs={'pk': self.sales_id.sales_prospect_id})

    def get_absolute_url_index(self):
        return reverse('Client:salescalllogindex', kwargs={'pk': self.sales_id.sales_prospect_id})

    @property
    def next_call(self):
        return '%s' % self.next_contact

    @property
    def full_details(self):
        """
        Gets client, call date and time.
        @return: client, call date and time.
        """
        return 'Client: %s Call Date: %s Time: %s' % (self.sales_id, self.call_date, self.call_time)

    @property
    def complete_details(self):
        return 'Client: %s Purpose: %s Call Date: %s Time: %s' % (self.sales_id, self.purpose,
                                                                  self.call_date, self.call_time)

        #endregion