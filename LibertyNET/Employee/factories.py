import factory
import factory.fuzzy
from models import Employee, Title
import Common.factories

#region work


class TitleFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Title
    title_id = 1
    title = 'S'

    #title = factory.Sequence(lambda n: "Title #%s" % n)


class EmployeeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Employee
    """
    address = Common.factories.AddressFactory.create()
    contact = Common.factories.ContactEmployeeFactory.create()
    print("ADDRESS+CONTACT ==>", address.id, contact.id)
    """
    employee_id = factory.sequence(lambda n: '81%d' % n)
    first_name = 'John'
    middle_initial = factory.fuzzy.FuzzyText(length=1)
    last_name = 'Smith'
    emp_number = factory.sequence(lambda n: '5678%d' % n)
    emp_address = factory.SubFactory(Common.factories.AddressFactory)
    emp_contact = factory.SubFactory(Common.factories.ContactEmployeeFactory)
    hire_date = '2014-01-13'
    pay_type = 'HR'
    pay_rate = factory.sequence(lambda n: '1%d.00' % n)

    @factory.post_generation
    def emp_title(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of groups passed in use them
            #[self.emp_title.add(title) for title in extracted]
            self.emp_title = Title.objects.all()
"""
    @classmethod
    def _prepare(cls, create, **kwargs):
        title = TitleFactory()
        title1 = TitleFactory(title_id=1, title='T')

        employee = super(EmployeeFactory, cls)._prepare(create, **kwargs)
        employee.emp_title.add(title)
        employee.emp_title.add(title1)
        return employee
"""


class EmployeeDjangoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Employee

    employee_id = factory.sequence(lambda n: '19%d' % n)
    first_name = 'John'
    middle_initial = factory.fuzzy.FuzzyText(length=1)
    last_name = 'Smith'
    emp_number = 1234
    emp_address = factory.lazy_attribute(lambda a: Common.factories.AddressFactory.create())
    emp_contact = factory.lazy_attribute(lambda a: Common.factories.ContactEmployeeFactory.create())
    hire_date = '2014-01-13'
    pay_type = 'HR'
    pay_rate = 12.00

    @classmethod
    def _prepare(cls, create, **kwargs):
        title = TitleFactory()
        employee = super(EmployeeDjangoFactory, cls)._prepare(create, **kwargs)
        employee.emp_title.add(title)
        if employee.employee_id:
           employee.emp_title = Title.objects.all()
        return employee


class EmployeeFactoryLatest(factory.DjangoModelFactory):
    FACTORY_FOR = Employee

    employee_id = factory.sequence(lambda n: '1234%d' % n)
    first_name = 'John'
    middle_initial = factory.fuzzy.FuzzyText(length=1)
    last_name = 'Smith'
    emp_number = 1234
    emp_address = factory.lazy_attribute(lambda a: Common.factories.AddressFactory.create())
    emp_contact = factory.lazy_attribute(lambda a: Common.factories.ContactEmployeeFactory.create())
    hire_date = '2014-01-13'
    pay_type = 'HR'
    pay_rate = 12.00

    @factory.post_generation
    def add_title(self, create, extracted, **kwargs):
        #all something like EmployeeFactoryLatest(emp_title = Title.objects.all())
        if extracted and type(extracted) == type(Title.objects.all()):
            self.emp_title = extracted
            self.save()
        else:
            if Title.objects.all().count() < 1:
                TitleFactory.create(title_id=4, title='M')
                TitleFactory.create(title_id=5, title='C')
            [self.emp_title.add(t) for t in Title.objects.all()]
            #for title in Title.objects.all():
             #   self.emp_title.add(title)


#endregion

