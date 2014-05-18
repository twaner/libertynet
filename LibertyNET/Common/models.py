from __builtin__ import property
from django.db import models
from django.utils.encoding import force_bytes
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from datetime import date
#from Common.helpermethods import boolean_helper


#region Choices

#This will be used to provide a drop down menu for any field that is a number in a range.
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

#region ModelManagers


class AddressManager(models.Manager):
    def create_address(self, street, unit, city, state, zip_code):
        """
        Creates an address.
        @rtype: Address.
        @param street: street info.
        @param unit: unit info.
        @param city: city name.
        @param state: state name.
        @param zip_code: zip code.
        @return: Address.
        """
        address = self.create(street=street, unit=unit, city=city,
                              state=state, zip_code=zip_code)
        address.save()
        return address


class ContactManager(models.Manager):
    def create_contact(self, phone, phone_extension, cell, office_phone, office_phone_extension,
                       email, work_email, website):
        """
        Creates a contact object.
        @rtype: Contact.
        @param phone: phone.
        @param phone_extension: extension.
        @param cell: cell.
        @param office_phone: office phone.
        @param office_phone_extension: extension.
        @param email: personal email.
        @param work_email: work email.
        @param website: website (optional).
        @return:
        """
        contact = self.create(phone=phone, phone_extension=phone_extension, cell=cell,
                              office_phone=office_phone, office_phone_extension=office_phone_extension,
                              email=email, work_email=work_email, website=website)
        contact.save()
        return contact

    def create_employee_contact(self, phone, cell, office_phone, office_phone_extension,
                                email, work_email):
        """
        Creates contact object for an employee
        @param phone: phone.
        @param cell: cell.
        @param email: email.
        @param work_email: work email.
        @return: employee based contact object.
        """
        contact = self.create(phone=phone, cell=cell, office_phone=office_phone,
                              office_phone_extension=office_phone_extension,
                              email=email, work_email=work_email)
        contact.save()
        return contact


class CallListManager(models.Manager):
    def create_call_list(self, first_name, middle_initial, last_name, cl_contact, cl_order,
                         cl_is_enabled, cl_genre):
        """
        Creates a call list object.
        @rtype: Call_List.
        @param cl_contact: contact info.
        @param cl_order: call list order.
        @param cl_is_enabled: call list's active status.
        @param cl_genre: call list's genre.
        @return:
        """
        call_list = self.create(first_name=first_name, last_name=last_name,
                                middle_initial=middle_initial.upper(), cl_contact=cl_contact,
                                cl_order=cl_order, cl_is_enabled=cl_is_enabled,
                                cl_genre=cl_genre)
        call_list.save()
        return call_list


class GenreManager(models.Manager):
    def create_genre(self, genre, genre_description):
        """
        Creates a genre.
        @rtype: Genre.
        @param genre: Type.
        @param genre_description: Description.
        @return: Genre object.
        """
        genre = self.create(genre=genre, genre_description=genre_description)
        genre.save()
        return genre


class BillingManager(models.Manager):
    def create_billing(self, profile_name, method, billing_address, card, ):
        """
        Creates a billing object.
        @rtype : Billing.
        @param profile_name: profile name.
        @param method: method.
        @param billing_address: address.
        @param card: card.
        @return: Billing object.
        """
        billing = self.create(profile_name=profile_name, method=method,
                              billing_address=billing_address, card=card)
        billing.save()
        return billing


class CardManager(models.Manager):
    def create_card(self, first_name, middle_initial, last_name, card_number, card_code, card_type, card_expiration):
        """
        Creates a Card object.
        @param first_name: first name.
        @param middle_initial: middle initial.
        @param last_name: last name.
        @param card_number: Card number.
        @param card_code: card code.
        @param card_type: type of card (ie Visa).
        @param card_expiration: Expiration Date.
        @rtype : Card
        @return: Card object.
        """
        card = self.create(first_name=first_name, middle_initial=middle_initial.upper(),
                           last_name=last_name, card_number=card_number, card_code=card_code,
                           card_type=card_type, card_expiration=card_expiration)
        card.save()
        return card


class InstallerManager(models.Manager):
    def create_installer(self, installer_code, installer_company_name, installer_notes):
        """
        Creates an installer Object
        @rtype: Installer.
        @param installer_code: code.
        @param installer_company_name: name.
        @param installer_notes: notes.
        @return: Installer Object.
        """
        installer = self.create(installer_code=installer_code, installer_company_name=installer_company_name,
                                installer_notes=installer_notes)
        installer.save()
        return installer


#endregion

#region BaseModels


class Person(models.Model):
    """
    Base class for any model that is a person.
    """
    first_name = models.CharField(max_length=30)
    middle_initial = models.CharField(max_length=2, blank=True, null=True)
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

    def __str__(self):
        return self.city_name


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
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30, choices=STATE_CHOICES, default='NY')
    zip_code = models.CharField("zip code", max_length=10)

    objects = AddressManager()

    def __str__(self):
        return (u'%s %s %s %s %s' % (self.street, self.unit,
                                     self.city, self.state, self.zip_code))


class Contact(models.Model):
    phone = models.CharField("primary phone", max_length=13, blank=True)
    phone_extension = models.CharField("primary phone extension", max_length=10, blank=True)
    cell = models.CharField("cell phone", max_length=12, blank=True)
    office_phone = models.CharField("office phone", max_length=13, blank=True)
    office_phone_extension = models.CharField("office phone extension", max_length=10, blank=True)
    email = models.EmailField(blank=True)
    work_email = models.EmailField(blank=True)
    website = models.URLField(blank=True)

    objects = ContactManager()

    def clean(self):
        super(Contact, self).clean()
        # Phone Extension with no phone (office and phone)
        if self.office_phone == '' and self.office_phone_extension != '':
            raise ValidationError('Please enter an Office Phone Number.')
        if self.phone == '' and self.phone_extension != '':
            raise ValidationError('Please enter a Phone Number.')

    def __str__(self):
        """
        Display for contact.
        @return: Formatted phone number.
        """
        return '%s%s%s-%s%s%s-%s%s%s%s' % tuple(self.phone)

    def cell_helper(self):
        """
        Display for contact.
        @return: Formatted phone number.
        """
        return '%s%s%s-%s%s%s-%s%s%s%s' % tuple(self.cell)

    def phone_extension_helper(self):
        """
        Helps create a readable phone number and extension.
        @return: a phone and extension if it exists.
        """
        if self.phone_extension is None or self.phone_extension == '':
            return "%s%s%s-%s%s%s-%s%s%s%s" % tuple(self.phone)
        else:
            phone = "%s%s%s-%s%s%s-%s%s%s%s" % tuple(self.phone)
            return '%s ext. %s' % (phone, self.phone_extension)

    def office_phone_extension_helper(self):
        """
        Helps create a readable phone number and extension.
        @return: a phone and extension if it exists.
        """
        if self.office_phone_extension is None or self.office_phone_extension == '':
            return "%s%s%s-%s%s%s-%s%s%s%s" % tuple(self.office_phone)
        else:
            phone = "%s%s%s-%s%s%s-%s%s%s%s" % tuple(self.office_phone)
            return '%s ext. %s' % (self.office_phone, self.office_phone_extension)


class CallList(Person):
    FIRST = 1
    SECOND = 2
    THIRD = 3
    FOURTH = 4
    FIFTH = 5
    SIXTH = 6
    SEVENTH = 7
    EIGHTH = 8
    NINTH = 9
    TENTH = 10
    NUMBER_CHOICES2 = (
        (FIRST, '1st'),
        (SECOND, '2nd'),
        (THIRD, '3rd'),
        (FOURTH, '4th'),
        (FIFTH, '5th'),
        (SIXTH, '6th'),
        (SEVENTH, '7th'),
        (EIGHTH, '8th'),
        (NINTH, '9th'),
        (TENTH, '10th'),
    )
    call_list_id = models.AutoField(primary_key=True)
    cl_contact = models.ForeignKey('Common.Contact')
    #2-16 ==> INTEGER => CHAR FIELD
    cl_order = models.CharField(choices=NUMBER_CHOICES2, max_length=11)
    cl_is_enabled = models.BooleanField(default=True)
    cl_genre = models.ForeignKey('Common.Genre')

    ordering = ['-cl_order']

    objects = CallListManager()

    def get_absolute_url(self):
        return reverse('Common.views.CallListDetails', args=[str(self.call_list_id)])

    @property
    def is_active(self):
        if self.cl_is_enabled:
            return "Active"
        else:
            return "Inactive"

    def __str__(self):
        return "%s %s" % (self.cl_genre, self.is_active)

    @property
    def order(self):
        return self.get_cl_order_display

    @property
    def calllist_contact_name(self):
        name = self.cl_contact
        print('NAME', name, type(name))
        return "%s %s %s" % (self.first_name, self.middle_initial, self.last_name)

    @property
    def calllist_order(self):
        return "%s" % self.cl_order


class Genre(models.Model):
    #TODO THIS WILL BE BURG, FIRE, CAMERA
    GENERAL = 'G'
    BURG = 'B'
    FIRE = 'F'
    MEDICAL = 'M'
    ENVIRONMENTAL = 'E'
    ALTERNATE = 'A'
    ALTERNATE2 = 'A2'
    genre_CHOICES = (
        (GENERAL, 'General Call List'),
        (BURG, "Burg Call List"),
        (FIRE, 'Fire Call List'),
        (MEDICAL, 'Medical Call List'),
        (ENVIRONMENTAL, 'Environmental Call List'),
        (ALTERNATE, 'Alternate Call List'),
        (ALTERNATE2, 'Alternate Call List 2'),)
    #Probably will do like Titles, in DB
    genre_id = models.AutoField(primary_key=True)
    genre = models.CharField(max_length=45)
    genre_description = models.CharField(max_length=144)

    objects = GenreManager()

    def __str__(self):
        return self.genre


class Billing(models.Model):
    """
    Billing connects to a client by client_id. Address and Contact are FK.
    Display changes based on business or not.
    """
    profile_name = models.CharField(max_length=45)
    # TODO - Handle this with a list
    method = models.IntegerField(max_length=11)
    billing_address = models.ForeignKey('Common.Address', null=True, blank=True)
    card = models.ForeignKey('Common.Card', null=True, blank=True)

    objects = BillingManager()

    def __unicode__(self):
        """
        Display for billing information.
        @return: business name or first and last name of client.
        """
        return u'%s' % self.profile_name

    def get_absolute_url_edit(self):
        return reverse('Client:editclientbilling', kwargs={'pk': self.id})


#TODO ==> Should this be company and then we make installer_code an attribute that is searched for?
class Installer(models.Model):
    installer_id = models.AutoField(primary_key=True)
    installer_code = models.IntegerField(max_length=11)
    installer_company_name = models.CharField(max_length=45)
    installer_notes = models.CharField(max_length=50)

    objects = InstallerManager()

    def __str__(self):
        return self.installer_company_name


class Card(Person):
    card_id = models.AutoField(primary_key=True)
    card_number = models.IntegerField(max_length=20)
    card_code = models.IntegerField(max_length=6)
    #TODO - Make dropdown list - research types
    card_type = models.CharField(max_length=14)
    card_expiration = models.DateField()
    #
    objects = CardManager()

    def get_model_fields(self):
        return self._meta.fields.name

    def get_fields(self):
        return [field.name for field in Card._meta.fields]

    def clean(self):
        super(Card, self).clean()
        # Is card expired?
        if self.card_expiration is not None:
            try:
                # Force dates to same format for valid comparison
                if self.card_expiration.strftime("%Y-%m-%d") <= date.today().strftime("%Y-%m-%d"):
                    raise ValidationError('Credit Card is expired')
            except TypeError:
                raise TypeError('Dates format invalid')

    def __str__(self):
        return 'Card Info: %s %s' % (self.first_name, self.last_name)


class CallLog(models.Model):
    caller = models.ForeignKey('Employee.Employee', null=True, blank=True)
    call_date = models.DateField()
    call_time = models.TimeField()
    purpose = models.CharField(max_length=150)
    notes = models.CharField(max_length=500)
    next_contact = models.DateField()
    ## 5/5/2014 - Added
    follow_up = models.BooleanField(default=False)
    #ALTER TABLE `libertynet11`.`Client_clientcalllog` ADD COLUMN `follow_up` TINYINT(1) NOT NULL  AFTER `client_id_id` ;
    #ALTER TABLE `libertynet11`.`Client_salesprospectcalllog` ADD COLUMN `follow_up` TINYINT(1) NOT NULL  AFTER `sales_id_id` ;

    def clean(self):
        pass

    class Meta:
        abstract = True

    @property
    def next_call(self):
        """
        Gets next contact time for client.
        @return: next contact time for client.
        """
        return '%s' % self.next_contact

    @property
    def call_date_time(self):
        return '%s %s' % (self.call_date, self.call_time)

    @property
    def requires_follow_up(self):
        """
        Is a follow_up required. Uses boolean_helper to handle.
        @return: boolean.
        """
        return self.follow_up


#endregion