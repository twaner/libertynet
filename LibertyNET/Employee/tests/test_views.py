from django.test import TestCase
from django.core.urlresolvers import reverse
from Common.helpermethods import assert_equals_worker, assert_in_worker
from Employee.factories import EmployeeFactoryLatest
from Employee.models import Employee


#region ViewTest


class TestEmployeeViews(TestCase):
    def setUp(self):
        emp = EmployeeFactoryLatest()
        self.assertIsInstance(emp, Employee)

    def test_employee_list_view(self):
        e = Employee.objects.get(emp_number=1234)
        url = reverse('Employee:index')
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, str(e.emp_number), resp.content)

    def test_employee_details_view(self):
        e = Employee.objects.get(emp_number=1234)
        url = reverse('Employee:details', kwargs={'pk': e.employee_id})
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, str(e.emp_number), resp.content)
        assert_in_worker(self, e.emp_address.street, resp.content)
        assert_in_worker(self, e.emp_contact.__str__(), resp.content)

    def test_add_employee_view(self):
        e = Employee.objects.get(emp_number=1234)
        url = reverse('Employee:addemployee')
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)

    def test_edit_employee_view(self):
        e = Employee.objects.get(emp_number=1234)
        url = reverse('Employee:editemployee', kwargs={'pk': e.employee_id})
        resp = self.client.get(url)

        assert_equals_worker(self, 200, resp.status_code)
        assert_in_worker(self, e.first_name, resp.content)
        assert_in_worker(self, e.emp_address.street, resp.content)
        assert_in_worker(self, e.emp_contact.phone, resp.content)

#endregion