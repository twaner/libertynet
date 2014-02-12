from django.test import TestCase
from Employee.models import Employee, Title
from Employee.helpermethods import titles_to_pk_list
from Employee.forms import AddEmployeeForm
from Employee.factories import EmployeeFactory, EmployeeDjangoFactory, EmployeeFactoryLatest, TitleFactory
from Common.models import Address, Contact
from Common.forms import AddressForm, EmployeeContactForm
from Common.factories import AddressFactory, ContactEmployeeFactory
import Common.helpermethods as chm

#region EmployeeTest


class EmployeeTest(TestCase):
    def setUp(self):
        print('Starting setup...')
        a = Address.objects.create(id=1111, street='44 Broadway', unit='4B', city='Kingston', state='NY',
                                   zip_code='12401')
        self.assertTrue(isinstance(a, Address), "Address not created")
        c = Contact.objects.create(id=2222, phone='8453334444', cell='8456667777',
                                   office_phone='9998883333', office_phone_extension='4545',
                                   email='test@test.com', work_email='work@work.com')
        self.assertTrue(isinstance(c, Contact), "Contact not created.")
        print('setup completed...')

    def test_create_employee(self):
        print('Starting test_create_employee...')
        address = Address.objects.get(pk=1111)
        contact = Contact.objects.get(pk=2222)
        title = TitleFactory()
        employee = Employee.objects.create(first_name='Jay', middle_initial='Q', last_name='Smith',
                                           emp_number=6969, hire_date='2013-01-13', pay_type='HR',
                                           pay_rate=12.99, emp_address=address, emp_contact=contact)
        employee.save()
        employee.emp_title.add(title)
        self.assertEqual(1, employee.emp_title.count(), 'title count is not 1.')
        self.assertTrue(isinstance(employee, Employee), 'test_create_employee is not Employee')

    def test_form(self):
        print('Starting test_form...')
        a = AddressFactory()
        self.assertTrue(isinstance(a, Address), "Is not Address => test_form")
        c = ContactEmployeeFactory()
        self.assertTrue(isinstance(c, Contact), "Is not Contact => test_form")
        title = TitleFactory.create(title_id=6, title="I")
        title2 = TitleFactory.create(title_id=3, title="O")
        e = EmployeeFactory.create(emp_title=(title, title2))
        #e = EmployeeFactoryLatest()
        self.assertTrue(isinstance(e, Employee), "Is not Employee ==> test_form")

        address_data = {'street': a.street, 'unit': a.unit, 'city': a.city, 'state': a.state,
                        'zip_code': a.zip_code,
        }
        contact_date = {
            'phone': c.phone, 'cell': c.cell, 'office_phone': c.office_phone,
            'office_phone_extension': c.office_phone_extension,
            'email': c.email, 'work_email': c.work_email,
        }

        e_title = titles_to_pk_list(e)
        employee_data = {
            'first_name': e.first_name, 'last_name': e.last_name, 'emp_number': e.emp_number,
            'emp_title': e_title,
            'hire_date': e.hire_date,
            'pay_type': e.pay_type, 'pay_rate': e.pay_rate,
        }
        # Generates and return a list of forms
        form_list = chm.form_generator(3)

        form_list[0] = AddressForm(data=address_data)
        form_list[1] = EmployeeContactForm(data=contact_date)
        form_list[2] = AddEmployeeForm(data=employee_data)
        # For debugging
        chm.form_errors_printer(form_list)

        self.assertTrue(form_list[0].is_valid())
        self.assertTrue(form_list[1].is_valid())
        self.assertTrue(form_list[2].is_valid())


        #test helper methods
        #TODO simulate request
        """
        a = cHM.create_address_helper(form_list[0])
        self.assertTrue(isinstance(a, Address),
                        "create_address_helper did not return Address")
        c = cHM.create_employee_contact_helper(form_list[1])
        self.assertTrue(isinstance(a, Contact),
                        "create_employee_contact_helper did not return Contact")
        employee_from_form = create_employee_helper(form_list[2]. a, c)
        self.assertTrue(isinstance(employee_from_form, Employee),
                        'create_employee_helper did not return Employee')
        """

#endregion


