from django.db import models
from django.core.exceptions import ValidationError
from Common.models import Person, Business
from Common.helpermethods import boolean_helper

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
        client = self.create(first_name=first_name, middle_initial=middle_initial, last_name=last_name,
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
        client = self.create(first_name=first_name, middle_initial=middle_initial, last_name=last_name,
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
        @param sp_liberty_contact: liberty employee who brought contact.
        @param sales_type: type of sale.
        @param sales_probability: estimate of sale's probability.
        @param initial_contact_date: contact date.
        @param comments: comments.
        @param sp_address: sales prospect's address (optional)
        @param sp_contact: sales prospect's contact info.
        @return: Sales Prospect.
        """
        sales_prospect = self.create(first_name=first_name, middle_initial=middle_initial, last_name=last_name,
                                     sp_business_name=sp_business_name, is_business=is_business,
                                     sp_liberty_contact=sp_liberty_contact,
                                     sales_type=sales_type, initial_contact_date=initial_contact_date,
                                     comments=comments, sp_address=sp_address,
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
        sales_prospect = self.create(first_name=first_name, middle_initial=middle_initial, last_name=last_name,
                                     sp_liberty_contact=sp_liberty_contact,
                                     sales_type=sales_type, initial_contact_date=initial_contact_date,
                                     comments=comments, sp_address=sp_address,
                                     sales_probability=sales_probability,
                                     sp_contact=sp_contact)
        sales_prospect.save()
        return sales_prospect

#endregion

#region Client Models


class Client(Person):
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
            return u'%s %s' % (self.first_name, self.last_name)

    def is_a_business(self):
        """
            Checks if a client is a commercial account.
            @return: Business name or first name of the client.
            """
        if self.is_business:
            return True
        else:
            return False

#endregion

#region Sales Prospects
class Sales_Prospect(Person):
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

    def clean(self):
        super(Sales_Prospect, self).clean()

    def __str__(self):
        """
        Sets display for Sales_Prospect object to first and last name.
        @return: first and last name of Sales_Prospect.
        """
        return u'%s %s' % (self.first_name, self.last_name)

        #endregion