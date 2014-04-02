from django.test import TestCase
from Employee.forms import *
from Employee.helpermethods import *
import Employee.factories as ef
import Common.helpermethods as chm
from Common.factories import AddressFactory, ContactEmployeeFactory
from Common.helpermethods import form_assert_false_worker, form_assert_true_worker, assert_true_worker, \
    assert_equals_worker, form_errors_printer
from Common.forms import AddressForm, EmployeeContactForm
from Common.models import Contact

#region FORM TESTS


class EmployeeFormTest(TestCase):
    print('Starting EmployeeFormTest....')

    def test_add_employee_form(self):
        title = ef.TitleFactory()
        title2 = ef.TitleFactory.create(title_id=3, title="O")
        e = ef.EmployeeFactory.create(emp_title=(title, title2))
        self.assertTrue(isinstance(e, Employee), "Is not Employee ==> test_form")

        e_title = titles_to_pk_list(e)
        print('e_title', e_title)
        employee_data = {
            'first_name': e.first_name, 'last_name': e.last_name, 'emp_number': e.emp_number,
            'emp_title': e_title,
            'hire_date': e.hire_date,
            'pay_type': e.pay_type, 'pay_rate': e.pay_rate,
        }

        form = AddEmployeeForm(data=employee_data)
        form_errors_printer(form)
        form_assert_true_worker(self, form)

        if form.is_valid():
            employee = create_employee_worker(form, AddressFactory(), ContactEmployeeFactory())
            assert_true_worker(self, Employee, employee)

    def test_form(self):
        print('Starting test_form...')
        a = AddressFactory()
        self.assertTrue(isinstance(a, Address), "Is not Address => test_form")
        c = ContactEmployeeFactory()
        self.assertTrue(isinstance(c, Contact), "Is not Contact => test_form")
        title = ef.TitleFactory.create(title_id=6, title="I")
        title2 = ef.TitleFactory.create(title_id=3, title="O")
        e = ef.EmployeeFactory.create(emp_title=(title, title2))
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

        if form_list[2].is_valid():
            employee = create_employee_worker(form_list[2], a, c)
            assert_true_worker(self, Employee, employee)

    def test_employee_form(self):
        title = ef.TitleFactory()
        title2 = ef.TitleFactory.create(title_id=3, title="O")
        e = ef.EmployeeFactory.create(first_name='John', emp_title=(title, title2))
        self.assertTrue(isinstance(e, Employee), "Is not Employee ==> test_form")
        assert_equals_worker(self, False, e.is_terminated)

        e_title = titles_to_pk_list(e)
        employee_data = {}
        form = AddEmployeeForm(data=employee_data)
        form_assert_false_worker(self, form)

        employee_data = {
            'first_name': e.first_name, 'last_name': e.last_name, 'emp_number': e.emp_number,
            'emp_title': e_title, 'termination_date': '2013-12-12', 'is_terminated': True,
            'hire_date': e.hire_date, 'termination_reason': 'Bad',
            'pay_type': e.pay_type, 'pay_rate': e.pay_rate,
        }

        form = EmployeeForm(data=employee_data)
        #form_errors_printer(form)
        form_assert_true_worker(self, form)
        if form.is_valid():
            update_employee(form, e, AddressFactory(), ContactEmployeeFactory())
            assert_true_worker(self, Employee, e)
            assert_equals_worker(self, True, e.is_terminated)




#endregion
