from django.db import models
from Common.models import Person, Business

#region Client Models

class Client(Person):
    client_id = models.AutoField(primary_key=True)
    client_number = models.IntegerField(max_length=10)
    business_name = models.CharField(max_length=50, blank=True)
    is_business = models.BooleanField(default=False)
    client_address = models.ForeignKey('Common.Address')
    client_contact = models.ForeignKey('Common.Contact')
    client_billing = models.ForeignKey('Common.Billing')
    client_date = models.DateField()
    clients = models.Manager()
    personal = PersonalManager()
    business = BusinessManager()

    def __unicode__(self):
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
            return self.business_name
        else:
            return self.first_name

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
    sp_business_name = models.CharField(max_length=50, blank=True)
    is_business = models.BooleanField(default=False)
    sp_liberty_contact = models.ForeignKey('Employee.Employee', verbose_name="Liberty employee" ,null=True, blank=True)
    sales_type = models.CharField(max_length=40, blank=True)
    sales_probability = models.CharField(choices=PROBABILITY)
    initial_contact_date = models.DateField(null=True, blank=True)
    comments = models.CharField(max_length=500, blank=True)
    sp_address = models.ForeignKey('common.Address', verbose_name="prospect address", null=True, blank=True)
    sp_contact = models.ForeignKey('common.Contact', verbose_name="prospect contact info", null=True, blank=True)
    is_client = models.BooleanField(default=False)

    def __unicode__(self):
        """
        Sets display for Sales_Prospect object to first and last name.
        @return: first and last name of Sales_Prospect.
        """
        return u'%s %s' % (self.first_name, self.last_name)

#endregion

#region ModelManagers

class ClientManager(models.Manager):
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

#endregion

#region Choices

#endregion