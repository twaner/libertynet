import factory
from models import Employee, Title
import Common.factories

#region work


class TitleFactory(factory.Factory):
    FACTORY_FOR = Title
    title_id = 11
    title = 'S'

    #title = factory.Sequence(lambda n: "Title #%s" % n)


class EmployeeFactory(factory.Factory):
    FACTORY_FOR = Employee
    employee_id = 9991
    first_name = 'John'
    last_name = 'Smith'
    emp_number = 1234
    emp_address = factory.lazy_attribute(lambda a: Common.factories.AddressFactory())
    emp_contact = factory.lazy_attribute(lambda b: Common.factories.ContactEmployeeFactory())
    hire_date = '2014-01-13'
    pay_type = 'HR'
    pay_rate = 12.00

    @factory.post_generation
    def titles(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return
        if extracted:
            # A list of groups passed in use them
            [self.groups.add(g) for g in extracted]

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
#endregion