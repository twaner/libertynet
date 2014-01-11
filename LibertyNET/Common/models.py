from django.db import models

#region BaseModels

class Person(models.Model):
    """
    Base class for any model that is a person.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)

    class Meta:
        abstract = True


class Business(Person):
    """
    Base class for any model that is strictly a business.
    """
    business_name = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        abstract = True


class City(models.Model):
    city_id = models.AutoField(primary_key=True)
    city_name = models.CharField(max_length=30)

    def __unicode__(self):
        return (self.city_name)


class State(models.Model):
    STATES = (
        ('Alabama', 'AL'),
        ('Alaska', 'AK'),
        ('Arizona', 'AZ'),
        ('Arkansas', 'AR'),
        ('California', 'CA'),
        ('Colorado', 'CO'),
        ('Connecticut', 'CT'),
        ('Delaware', 'DE'),
        ('District of Columbia', 'DC'),
        ('Florida', 'FL'),
        ('Georgia', 'GA'),
        ('Hawaii', 'HI'),
        ('Idaho', 'ID'),
        ('Illinois', 'IL'),
        ('Indiana', 'IN'),
        ('Iowa', 'IA'),
        ('Kansas', 'KS'),
        ('Kentucky', 'KY'),
        ('Louisiana', 'LA'),
        ('Maine', 'ME'),
        ('Maryland', 'MD'),
        ('Massachusetts', 'MA'),
        ('Michigan', 'MI'),
        ('Minnesota', 'MN'),
        ('Mississippi', 'MS'),
        ('Missouri', 'MO'),
        ('Montana', 'MT'),
        ('Nebraska', 'NE'),
        ('Nevada', 'NV'),
        ('New Hampshire', 'NH'),
        ('New Jersey', 'NJ'),
        ('New Mexico', 'NM'),
        ('New York', 'NY'),
        ('North Carolina', 'NC'),
        ('North Dakota', 'ND'),
        ('Ohio', 'OH'),
        ('Oklahoma', 'OK'),
        ('Oregon', 'OR'),
        ('Pennsylvania', 'PA'),
        ('Rhode Island', 'RI'),
        ('South Carolina', 'SC'),
        ('South Dakota', 'SD'),
        ('Tennessee', 'TN'),
        ('Texas', 'TX'),
        ('Utah', 'UT'),
        ('Vermont', 'VT'),
        ('Virginia', 'VA'),
        ('Washington', 'WA'),
        ('West Virginia', 'WV'),
        ('Wisconsin', 'WI'),
        ('Wyoming', 'WY'),
    )
    #state_id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=2, choices=STATES)

    def __unicode__(self):
        return (self.state)


class Address(models.Model):
    """
    Address model. State options limited by State_Choices.
    """
    street = models.CharField("street address", max_length=30)
    unit = models.CharField("unit address", max_length=30, blank=True)
    city = models.ForeignKey(City, blank=True)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default='NY')
    zip_code = models.CharField("zip code", max_length=10)

    def __unicode__(self):
        return (u'%s %s %s %s %s' % (self.address, self.address2,
                                     self.city.city_name, self.state, self.zip_code))


class Contact(models.Model):
    phone = models.CharField("primary phone", max_length=13, blank=True)
    phone_extension = models.CharField("primary phone extension", max_length=10, blank=True)
    cell = models.CharField("cell phone", max_length=12, blank=True)
    office_phone = models.CharField("office phone", max_length=13, blank=True)
    office_phone_extension = models.CharField("office phone extension", max_length=10, blank=True)
    email = models.EmailField(blank=True)
    work_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    def __unicode__(self):
        """
        Display for contact.
        @return: Formatted phone number.
        """
        return "%s%s%s-%s%s%s-%s%s%s%s" % tuple(self.phone)

    def phone_extension_helper(self):
        """
        Helps create a readable phone number and extension.
        @return: a phone and extension if it exists.
        """
        if self.phone_extension is None:
            return "%s%s%s-%s%s%s-%s%s%s%s" % tuple(self.phone)
        else:
            return "%s%s%s-%s%s%s-%s%s%s%s" % tuple(self.phone),
        " ", self.phone_extension


class Call_List(models.Model):
    call_list_id = models.AutoField(primary_key=True)
    cl_contact = models.ForeignKey('Common.Contact')
    cl_order = models.IntegerField(choices=NUMBER_CHOICES)
    cl_is_enabled = models.BooleanField(default=True)
    cl_type = models.ForeignKey('Common.Type')

    #TODO - def __unicode__(self):


class Type(models.Model):
    #TODO THIS WILL BE BURG, FIRE, CAMERA
    GENERAL = 'G'
    BURG = 'B'
    FIRE = 'F'
    MEDICAL = 'M'
    ENVIRONMENTAL = 'E'
    ALTERNATE = 'A'
    ALTERNATE2 = 'A2'
    TYPE_CHOICES = (
        (GENERAL, 'General Call List'),
        (BURG, "Burg Call List"),
        (FIRE, 'Fire Call List'),
        (MEDICAL, 'Medical Call List'),
        (ENVIRONMENTAL, 'Environmental Call List'),
        (ALTERNATE, 'Alternate Call List'),
        (ALTERNATE2, 'Alternate Call List 2'),
    #Probably will do like Titles, in DB
    type_id = models.AutoField(primary_key=True)
    type = models.CharField(max_length=45)
    type_description = models.CharField(max_length=144)

    #TODO - def __unicode__(self):


class Billing(models.Model):
    """
    Billing connects to a client by client_id. Adddress and Contact are FK.
    Display changes based on business or not.
    """
    client_id = models.ForeignKey('Client.Client')
    profile_name = models.CharField(max_length=45)
    method = models.IntegerField(max_length=11)
    billing_address = models.ForeignKey('Common.Address', null=True, blank=True)
    billing_contact = models.ForeignKey('Common.Contact', null=True, blank=True)
    card = models.ForeignKey('Common.Card', null=True, blank=True)
    is_business = models.BooleanField(default=False)

    def __unicode__(self):
        """
        Display for billing information.
        @return: business name or first and last name of client.
        """
        if self.is_business == True:
            return (self.business_name)
        else:
            return (u'%s %s' % (self.attention_first_name, self.attention_last_name))


#TODO ==> Should this be comapny and then we make installer_code an attribute that is searched for?
class Installer(models.Model):
    installer_id = models.AutoField(primary_key=True)
    installer_code = models.IntegerField(max_length=11)
    installer_company_name = models.CharField(max_length=45)
    installer_notes = models.CharField(max_length=50)


#endregion

#region Choices

#This will be used to provide a dropdown menu for any field that is a number in a range.
NUMBER_CHOICES = (
    (1, '1st'),
    (2, '2nd'),
    (3, '3rd'),
    (4, '4th'),
    (5, '5th'),
    (6, '6th'),
    (7, '7th'),
    (8, '8th'),
    (9, '9th'),
    (10, '10th'),
)

STATE_CHOICES = (
    ('Alabama', 'AL'),
    ('Alaska', 'AK'),
    ('Arizona', 'AZ'),
    ('Arkansas', 'AR'),
    ('California', 'CA'),
    ('Colorado', 'CO'),
    ('Connecticut', 'CT'),
    ('Delaware', 'DE'),
    ('District of Columbia', 'DC'),
    ('Florida', 'FL'),
    ('Georgia', 'GA'),
    ('Hawaii', 'HI'),
    ('Idaho', 'ID'),
    ('Illinois', 'IL'),
    ('Indiana', 'IN'),
    ('Iowa', 'IA'),
    ('Kansas', 'KS'),
    ('Kentucky', 'KY'),
    ('Louisiana', 'LA'),
    ('Maine', 'ME'),
    ('Maryland', 'MD'),
    ('Massachusetts', 'MA'),
    ('Michigan', 'MI'),
    ('Minnesota', 'MN'),
    ('Mississippi', 'MS'),
    ('Missouri', 'MO'),
    ('Montana', 'MT'),
    ('Nebraska', 'NE'),
    ('Nevada', 'NV'),
    ('New Hampshire', 'NH'),
    ('New Jersey', 'NJ'),
    ('New Mexico', 'NM'),
    ('New York', 'NY'),
    ('North Carolina', 'NC'),
    ('North Dakota', 'ND'),
    ('Ohio', 'OH'),
    ('Oklahoma', 'OK'),
    ('Oregon', 'OR'),
    ('Pennsylvania', 'PA'),
    ('Rhode Island', 'RI'),
    ('South Carolina', 'SC'),
    ('South Dakota', 'SD'),
    ('Tennessee', 'TN'),
    ('Texas', 'TX'),
    ('Utah', 'UT' ),
    ('Vermont', 'VT'),
    ('Virginia', 'VA'),
    ('Washington', 'WA'),
    ('West Virginia', 'WV'),
    ('Wisconsin', 'WI'),
    ('Wyoming', 'WY'),
)

#endregion