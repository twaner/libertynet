from django.test import TestCase
from models import Employee, Title
from helpermethods import create_employee_helper
from Common.models import Contact, Address


#class Employee Tests


class EmployeeTest(TestCase):
    def setUp(self):
        Address.objects.create(street="44 Broadway", unit="4B", city="Kingston", state="NY",
                               zip_code="12401")
        Contact.objects.create(phone="8453334444", cell="8456667777",
                               email="test@test.com", work_email="work@work.com")

    def test_employee_creation(self):
        address = Address.objects.get(unit="4B")
        contact = Contact.objects.get(phone="8453334444")
        title = Title(title="S")
        title1 = Title(title="M")
        print("TITLE1==>", type(title))
        title_list = [title, title1]
        e = Employee.objects.create(first_name="John", last_name="Smith", emp_number=1234, emp_title=title_list,
                                    emp_address=address, emp_contact=contact, hire_date=2014 - 01 - 13,
                                    pay_type="HR", pay_rate=12.00)

        self.assertTrue(isinstance(e, Employee), "Is not Employee")

#endregion

"""    def create_employee(self, first_name="John", last_name="Smith", emp_number=1234,
                                         emp_address=address, emp_contact=contact, hire_date=2014-01-13,
                                         pay_type="HR", pay_rate=12.00, emp_title=title_list):
        return Employee.objects.create_employee(first_name=first_name, last_name=last_name,
                                                emp_number=emp_number, emp_address=emp_address,
                                                emp_contact=emp_contact, hire_date=hire_date,pay_type=pay_type,
                                                pay_rate=pay_rate, emp_title=emp_title)
"""