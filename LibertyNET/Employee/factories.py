import factory
from models import Employee, Title
import Common.factories

#region work


class TitleFactory(factory.Factory):
    FACTORY_FOR = Title
    title_id = 1
    title = 'S'

    #title = factory.Sequence(lambda n: "Title #%s" % n)


class EmployeeFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Employee

    employee_id = factory.sequence(lambda n: '999%d' % n)
    first_name = 'John'
    last_name = 'Smith'
    emp_number = 1234
    emp_address = factory.lazy_attribute(lambda a: Common.factories.AddressFactory())
    emp_contact = factory.lazy_attribute(lambda b: Common.factories.ContactEmployeeFactory())
    hire_date = '2014-01-13'
    pay_type = 'HR'
    pay_rate = 12.00

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
        title1 = TitleFactory(title_id=12, title='T')

        employee = super(EmployeeFactory, cls)._prepare(create, **kwargs)
        employee.emp_title.add(title)
        employee.emp_title.add(title1)
        return employee
"""


class EmployeeDjangoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Employee

    employee_id = factory.sequence(lambda n: '888%d' % n)
    first_name = 'John'
    last_name = 'Smith'
    emp_number = 1234
    emp_address = factory.lazy_attribute(lambda a: Common.factories.AddressFactory())
    emp_contact = factory.lazy_attribute(lambda a: Common.factories.ContactEmployeeFactory())
    hire_date = '2014-01-13'
    pay_type = 'HR'
    pay_rate = 12.00

    @classmethod
    def _prepare(cls, create, **kwargs):
        title = TitleFactory()
        employee = super(EmployeeDjangoFactory, cls)._prepare(create, **kwargs)
        #employee.emp_title.add(title)
        if employee.employee_id:
            employee.emp_title = Title.objects.all()
        return employee


class EmployeeFactoryLatest(factory.Factory):
    FACTORY_FOR = Employee

    employee_id = factory.sequence(lambda n: '1234%d' % n)
    first_name = 'John'
    last_name = 'Smith'
    emp_number = 1234
    emp_address = factory.lazy_attribute(lambda a: Common.factories.AddressFactory())
    emp_contact = factory.lazy_attribute(lambda a: Common.factories.ContactEmployeeFactory())
    hire_date = '2014-01-13'
    pay_type = 'HR'
    pay_rate = 12.00

    @factory.post_generation
    def add_title(self, create, extracted, **kwargs):
        #all something like EmployeeFactoryLatest(emp_title = Title.objects.all())
        if extracted and type(extracted) == type(Title.objects.all()):
            self.emp_title = extracted
            self.save()
            print('add_title IF')
        else:
            print('add_title ELSE')
            if Title.objects.all().count() < 1:
                TitleFactory.create(title_id=4, title='M')
                TitleFactory.create(title_id=5, title='M')
                print("TITLE OBJ COUNT ", Title.objects.all().count())
                print('add_title ELSE into IF')
            for title in Title.objects.all():
                self.emp_title.add(title)
                print('add_title ELSE into FOR')


#endregion

