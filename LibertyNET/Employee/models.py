from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from Common.models import Person

#region ModelManagers


class EmployeeManager(models.Manager):
    def create_employee(self, first_name, middle_initial, last_name, emp_number, emp_title, emp_address, emp_contact,
                        hire_date, pay_type, pay_rate, is_terminated, termination_date, termination_reason):
        """
        Creates a new employee. Terminated attributes are False and None by default.
        @param first_name: employee's first name
        @param middle_initial: employee's middle initial.
        @param last_name: employee's last name.
        @param emp_number: employee number.
        @param emp_title: employee title will be requests list.
        @param emp_address: employee address.
        @param emp_contact: employee contact.
        @param hire_date: employee's hire date.
        @param pay_type: employee's pay type.
        @param pay_rate: employee's pay rate.
        @param is_terminated: is employee terminated (False).
        @param termination_date: employee termination date (None).
        @param termination_reason: employee termination reason (None).
        @return:
        """

        employee = self.create(first_name=first_name, last_name=last_name, middle_initial=middle_initial.upper(),
                               emp_number=emp_number, emp_title=emp_title, emp_address=emp_address,
                               emp_contact=emp_contact, hire_date=hire_date, pay_type=pay_type,
                               pay_rate=pay_rate,
                               is_terminated=False, termination_date=None, termination_reason=None)
        print("EMP_TITLE==>", type(emp_title))
        employee.save(commit=False)
        [employee.emp_title.add(et) for et in emp_title]
        employee.save()
        return employee

    def create_employee(self, first_name, middle_initial, last_name, emp_number, emp_title, emp_address, emp_contact,
                        hire_date, pay_type, pay_rate):
        """
        Creates a new employee. Terminated attributes are False and None by default.
        @param first_name: employee's first name
        @param middle_initial: employee's middle initial.
        @param last_name: employee's last name.
        @param emp_number: employee number.
        @param emp_title: employee title will be requests list.
        @param emp_address: employee address.
        @param emp_contact: employee contact.
        @param hire_date: employee's hire date.
        @param pay_type: employee's pay type.
        @param pay_rate: employee's pay rate.
        @param is_terminated: is employee terminated (False).
        @param termination_date: employee termination date (None).
        @param termination_reason: employee termination reason (None).
        @return:
        """
        employee = self.create(first_name=first_name, last_name=last_name, middle_initial=middle_initial.upper(),
                               emp_number=emp_number, emp_title=emp_title, emp_address=emp_address,
                               emp_contact=emp_contact, hire_date=hire_date, pay_type=pay_type,
                               pay_rate=pay_rate)

        print("EMP_TITLE==>", type(emp_title))
        employee.save(commit=False)
        [employee.emp_title.add(et) for et in emp_title]
        employee.save()
        return employee


#endregion

#region Models


class Title(models.Model):
    SALES = 'S'
    TECHNICIAN = 'T'
    OFFICE = 'O'
    MARKETING = 'M'
    CONTRACTOR = 'C'
    INTERN = 'I'
    TITLE_CHOICES = (
        (SALES, "Sales"),
        (TECHNICIAN, "Technician"),
        (OFFICE, "Office"),
        (MARKETING, "Marketing"),
        (CONTRACTOR, "Contractor"),
        (INTERN, "Intern"),
    )
    title_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=2, choices=TITLE_CHOICES)

    def __str__(self):
        """
        Used to display names of the titles.
        @return: title names.
        """
        return self.get_title_display()


#endregion

#region Employee class


class Employee(Person):
    """
    Employee model. To add titles use e.emp_title.add(t).
    """
    PAY_TYPE_CHOICES = (
        ('COM', 'Commission'),
        ('HR', 'Hourly'),
        ('SAL', 'Salary'),
        ('OT', 'Other'),
        ('NP', 'Non-Paid'),
    )
    employee_id = models.AutoField(primary_key=True)
    emp_number = models.IntegerField(max_length=10)
    emp_title = models.ManyToManyField(Title, verbose_name="Employee Title")
    emp_address = models.ForeignKey('Common.Address')
    emp_contact = models.ForeignKey('Common.Contact')
    hire_date = models.DateField()
    pay_type = models.CharField(choices=PAY_TYPE_CHOICES, default='HR', max_length=12)
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    is_terminated = models.BooleanField(default=False)
    termination_date = models.DateField(null=True, blank=True, default=None)
    termination_reason = models.CharField(max_length=300, blank=True, null=True)

    objects = EmployeeManager()

    def get_absolute_url(self):
        return reverse('Employee:details', kwargs={'pk': self.employee_id})

    def get_absolute_url_edit(self):
        return reverse('Employee:editemployee', kwargs={'pk': self.employee_id})

    def clean(self):
        super(Employee, self).clean()
        # print('is term /// term reason // term date', self.is_terminated,
        #       self.termination_reason, self.termination_date)
        #if self.is_terminated or self.termination_reason is not None or self.termination_date is not None:
        if self.is_terminated and self.termination_reason is not None and self.termination_date is not None or \
                self.is_terminated is False and self.termination_reason is None and self.termination_date is None:
            pass
        else:
            raise ValidationError('Please fill out all termination fields.')

    def __str__(self):
        """
        Displays first and last of Employee
        @return: Employee first and last name.
        """
        return u'%s %s %s' % (self.first_name, self.middle_initial, self.last_name)

    @property
    def worker_is(self):
        """
        Displays titles.
        @rtype : Title.
        @return: Titles for Employee
        """
        return self.emp_title.all()

#endregion
