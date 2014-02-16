from django.test import TestCase
from django.core.exceptions import ValidationError
from Employee.models import Employee
from Employee.factories import EmployeeFactory, TitleFactory
from Common.models import Address, Contact
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
        chm.assert_equals_worker(self, 1, employee.emp_title.count())
        self.assertTrue(isinstance(employee, Employee), 'test_create_employee is not Employee')
        chm.assert_equals_worker(self,
                                 ('%s %s %s' % (employee.first_name, employee.middle_initial, employee.last_name)),
                                 employee.__str__())
        abs_url = '/employee/%s/' % employee.employee_id
        abs_url_edit = '/employee/editemployee/%s/' % employee.employee_id
        print('%%%', employee.worker_is, type(employee.worker_is))

        chm.assert_equals_worker(self, abs_url, employee.get_absolute_url())
        chm.assert_equals_worker(self, abs_url_edit, employee.get_absolute_url_edit())

    def test_employee_clean(self):
        employee = Employee()
        self.assertRaises(ValidationError, employee.clean())

    def test_employee_clean_data(self):
        employee = EmployeeFactory()
        employee.is_terminated = True
        self.assertRaisesMessage(ValidationError, 'Please fill out all termination fields.')
        employee.is_terminated = False
        employee.termination_reason = 'Bad'
        self.assertRaisesMessage(ValidationError, 'Please fill out all termination fields.')
        employee.is_terminated = True
        employee.termination_reason = 'Reason'
        employee.termination_date = '2014-1-23'
        employee.clean()


#endregion


