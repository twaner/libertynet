from django.test import TestCase
from Employee.forms import *
from Employee.helpermethods import *
import Employee.factories as f
import Common.helpermethods as CHM

#region FORM TESTS


class EmployeeFormTest(TestCase):
    print('Starting EmployeeFormTest....')

    def test_employee_form(self):
        title = f.TitleFactory()
        title2 = f.TitleFactory.create(title_id=3, title="O")
        e = f.EmployeeFactory.create(emp_title=(title, title2))
        self.assertTrue(isinstance(e, Employee), "Is not Employee ==> test_form")

        e_title = titles_to_pk_list(e)
        employee_data = {
            'first_name': e.first_name, 'last_name': e.last_name, 'emp_number': e.emp_number,
            'emp_title': e_title,
            'hire_date': e.hire_date,
            'pay_type': e.pay_type, 'pay_rate': e.pay_rate,
        }
        # Generates and return a list of forms
        form_list = CHM.form_generator(1)

        form_list[0] = AddEmployeeForm(data=employee_data)
        # For debugging
        CHM.form_errors_printer(form_list)

        self.assertTrue(form_list[0].is_valid())

#endregion
