from django.test import TestCase
from models import Employee, Title
from forms import AddEmployeeForm
from factories import EmployeeFactory, TitleFactory
from Common.forms import AddressForm, EmployeeContactForm
from Common.factories import AddressFactory, ContactEmployeeFactory
from helpermethods import create_employee_helper
from Common.models import Contact, Address
import Common.helpermethods as CHM

#class Employee Tests


class EmployeeTest(TestCase):
    def setUp(self):
        a = Address.objects.create(street='44 Broadway', unit='4B', city='Kingston', state='NY',
                                   zip_code='12401')
        self.assertTrue(isinstance(a, Address), "Address not created")
        c = Contact.objects.create(phone='8453334444', cell='8456667777',
                                   email='test@test.com', work_email='work@work.com')
        self.assertTrue(isinstance(c, Contact), "Contact not created.")

    def test_form(self):
        a = AddressFactory()
        self.assertTrue(isinstance(a, Address), "Is not Address => test_form")
        c = ContactEmployeeFactory()
        self.assertTrue(isinstance(c, Contact), "Is not Contact => test_form")
        e = EmployeeFactory()
        self.assertTrue(isinstance(e, Employee), "Is not Employee ==> test_form")

        address_data = {'street': a.street, 'unit': a.unit, 'city': a.city, 'state': a.state,
                        'zip_code': a.zip_code,
                        }
        contact_date = {
            'phone': c.phone, 'cell': c.cell, 'email': c.email, 'work_email': c.work_email,
        }
        employee_data = {
            'first_name': e.first_name, 'last_name': e.last_name, 'emp_number': e.emp_number,
            'emp_title': e.emp_title,
            'hire_date': e.hire_date,
            'pay_type': e.pay_type, 'pay_rate': e.pay_rate,
        }

        form_list = CHM.form_generator(3)

        form_list[0] = AddressForm(data=address_data)
        form_list[1] = EmployeeContactForm(data=contact_date)
        form_list[2] = AddEmployeeForm(data=employee_data)

        CHM.form_errors_printer(form_list)

        self.assertTrue(form_list[0].is_valid())
        self.assertTrue(form_list[1].is_valid())
        self.assertTrue(form_list[2].is_valid())




#endregion

#region Factory Tests


class TestFactory(TestCase):
    def test_employee_factory(self):
        employee = EmployeeFactory()
        self.assertTrue(isinstance(employee, Employee), "EmployeeFactory() is not Employee!")

    def test_title_factory(self):
        title = TitleFactory(title_id=69, title="I")
        self.assertTrue(isinstance(title, Title), "TitleFactory() is not Title!")
        self.assertEqual(title.title_id, 69, "title_id not equal")
        self.assertEqual(title.title, 'I', "title is not equal")

    def full_employee_factory(self):
        title = TitleFactory(title_id=69, title="I")
        title2 = TitleFactory(title_id=99, title="O")
        self.assertNotEqual(title.title, title2.title, "Titles are the same")
        employee = EmployeeFactory.create(titles=(title, title2))
        self.assertTrue(isinstance(employee, Employee), "EmployeeFactory() is not Employee!")
        self.assertTrue(employee.emp_title.count(), 2, "Title Count does not match")

#endregion

"""    def create_employee(self, first_name="John", last_name="Smith", emp_number=1234,
                                         emp_address=address, emp_contact=contact, hire_date=2014-01-13,
                                         pay_type="HR", pay_rate=12.00, emp_title=title_list):
        return Employee.objects.create_employee(first_name=first_name, last_name=last_name,
                                                emp_number=emp_number, emp_address=emp_address,
                                                emp_contact=emp_contact, hire_date=hire_date,pay_type=pay_type,
                                                pay_rate=pay_rate, emp_title=emp_title)
employee = EmployeeFactory()
        self.assertTrue(isinstance(employee, Employee), "EmployeeFactory() is not Employee!")


"""