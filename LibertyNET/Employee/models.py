from django.db import models
from Common.models import Person

#region Employee Attributes
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

    def __unicode__(self):
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
    pay_type = models.CharField(choices=PAY_TYPE_CHOICES, default='HR')
    pay_rate = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    is_terminated = models.BooleanField(default=False)
    termination_date = models.DateField(null=True, blank=True)
    termination_reason = models.CharField(max_length=300, blank=True)

    def __unicode__(self):
        """
        Displays first and last of Employee
        @return: Employee first and last name.
        """
        return u'%s %s' % (self.first_name, self.last_name)

    def worker_is(self):
        """
        Displays titles.
        @return: Titles for Employee
        """
        return (self.e_title)

#end region

#region Employee Managers
#TODO Add Managers
#endregion