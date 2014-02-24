from django.test import TestCase
from Work.factories import JobFactory, TaskFactory, TicketFactory, WageFactory
from Work.models import Job, Task, Ticket, Wage
from Common.models import Address, Contact
import Common.helpermethods as chm
from Employee.factories import EmployeeFactory
from Employee.models import Employee
from Client.factories import ClientFactory
from Client.models import Client
from Site.factories import SystemFactory
from datetime import date, timedelta, datetime

#region globals

date1 = date.today()
date2 = date.today() + timedelta(hours=5)
time1 = chm.time_str_to_time('09:00')
time2 = chm.time_str_to_time('14:45')
lun1 = chm.time_str_to_time('12:00')
lun2 = chm.time_str_to_time('12:45')
lunch_start = chm.time_str_to_time('12:00')
lunch_end = chm.time_str_to_time('13:00')
#print('TIME_STR_TO_TIME', time1, time2, type(time1))

dt1 = timedelta(hours=time1.hour, minutes=time1.minute)
dt2 = timedelta(hours=time2.hour, minutes=time2.minute)
#print('D1///D2', dt1, dt2, type(dt1))
qq = dt2 - dt1
day = chm.time_worker(time2) - chm.time_worker(time1)
lunch = chm.time_diff(lun1, lun2) #chm.time_worker(lun2) - chm.time_worker(lun1)
#print('TYPES', type(day), type(lunch))
#print('adding two timedelta', qq, type(qq), str(qq), '.SECONDS: ', qq.seconds)
ff = datetime.combine(date.today(), time1)
#print('datetime.combine', ff, type(ff))

work_day = datetime.combine(date.today(), time2) - datetime.combine(date.today(), time1)
#print('Combine', work_day, type(work_day))

#print('workday properties', work_day.seconds)

work_time = day - lunch
#print('TYPE WORK_TIME', type(work_time))
time_worked = chm.seconds_to_hours(work_time)
sal = 14.75
pay = sal * time_worked

#print('time_worked, sal, pay', type(time_worked), time_worked, sal, pay)

#endregion

#region WorkFactory Tests


class WorkFactoryTests(TestCase):
    print('Starting WorkFactoryTests...')

    def test_job_factory(self):
        job = JobFactory()
        self.assertTrue(isinstance(job, Job), 'JobFactory is not Job')

    def test_task_factory(self):
        task = TaskFactory()
        self.assertTrue(isinstance(task, Task), 'TaskFactory is not Task')

    def test_ticket_factory(self):
        ticket = TicketFactory()
        self.assertTrue(isinstance(ticket, Ticket), 'TicketFactory is not Ticket')

    def test_wage_factory(self):
        wage = WageFactory()
        self.assertTrue(isinstance(wage, Wage), 'WageFactory is not Wage')


class WorkTests(TestCase):
    def setUp(self):
        print('Starting setup...')
        a = Address.objects.create(id=1111, street='44 Broadway', unit='4B', city='Kingston', state='NY',
                                   zip_code='12401')
        self.assertTrue(isinstance(a, Address), "Address not created")
        c = Contact.objects.create(id=2222, phone='8453334444', cell='8456667777',
                                   office_phone='9998883333', office_phone_extension='4545',
                                   email='test@test.com', work_email='work@work.com')
        self.assertTrue(isinstance(c, Contact), "Contact not created.")

        e = EmployeeFactory(employee_id=9887)#(first_name='John')
        e2 = EmployeeFactory(employee_id=3445)
        c = ClientFactory(client_id=8877)
        print('setup completed...')

    def test_job(self):
        address = Address.objects.get(pk=1111)
        employee = Employee.objects.get(employee_id=9887)
        client = Client.objects.get(client_id=8877)
        emp_list = [employee]

        job = Job.objects.create_job('job name,', 3344, client, address, emp_list)
        chm.assert_true_worker(self, Job, job)
        chm.assert_equals_worker(self, len(emp_list), job.job_employee.count())
        return job

    def test_ticket(self):
        employee = Employee.objects.get(employee_id=9887)
        employee2 = Employee.objects.get(employee_id=3445)
        contact = Contact.objects.get(pk=2222)
        system = SystemFactory()
        job = self.test_job()
        time = '09:00'
        emp_list = [employee, employee2]

        ticket = Ticket.objects.create_ticket(date1, time, job, system, 'ticket description', 'ticket notes', date1,
                                              time1, date1, time2, contact, 'ticket signature', True, emp_list)

        chm.assert_true_worker(self, Ticket, ticket)
        chm.assert_equals_worker(self, len(emp_list), ticket.ticket_employee.count())
        return ticket

    def test_task(self):
        employee = Employee.objects.get(employee_id=9887)
        employee2 = Employee.objects.get(employee_id=3445)
        ticket = self.test_ticket()
        employee3 = EmployeeFactory(employee_id=7667)

        emp_list = [employee, employee2, employee3]

        task = Task.objects.create_task(ticket, 'task name', date1, employee, 1, True,
                                        employee, date1, 'task notes')
        chm.assert_true_worker(self, Task, task)
        #chm.assert_equals_worker(self, len(emp_list), task.task_employee.count())
        return task

    def test_wages(self):
        employee = Employee.objects.get(employee_id=9887)
        time11 = '09:00'
        time22 = '14:45'
        lun11 = '12:00'
        lun22 = '12:45'
        wage = Wage.objects.create_wage(wages_employee=employee, wage_date=date1, start_time=time11,
                                        lunch_start=lun11, lunch_end=lun22, end_time=time22, hourly_rate=15.00)

        lunch1 = chm.time_diff(wage.lunch_start, wage.lunch_end)
        chm.assert_true_worker(self, Wage, wage)
        chm.assert_equals_worker(self, 75.0, wage.gross_wage)
        chm.assert_equals_worker(self, 5.0, wage.total_hours)
        chm.assert_true_non_instance_worker(self, wage.took_lunch)
        chm.assert_equals_worker(self, lunch1, wage.lunch_time)

        #print('test_wages: gross wage/hours/pay', wage.gross_wage, wage.total_hours, wage.hourly_rate)

    def test_wages_no_lunch(self):
        employee = Employee.objects.get(employee_id=9887)
        time11 = '09:00'
        time22 = '14:45'
        lun11 = '12:00'
        lun22 = '12:45'
        wage = Wage.objects.create_wage(wages_employee=employee, wage_date=date1, start_time=time11,
                                        lunch_start=None, lunch_end=None, end_time=time22, hourly_rate=15.00)
        lunch1 = chm.time_diff(wage.lunch_start, wage.lunch_end)
        chm.assert_true_worker(self, Wage, wage)
        chm.assert_equals_worker(self, 86.25, wage.gross_wage)
        chm.assert_equals_worker(self, 5.75, wage.total_hours)
        chm.assert_false_non_instance_worker(self, wage.took_lunch)
        chm.assert_equals_worker(self, lunch1, wage.lunch_time)

        #print('test_wages_no_lunch: gross wage/hours/pay', wage.gross_wage, wage.total_hours, wage.hourly_rate)

    def test_wages_no_end_lunch(self):
        employee = Employee.objects.get(employee_id=9887)
        time11 = '09:00'
        time22 = '14:45'
        lun11 = '12:00'
        lun22 = '12:45'
        wage = Wage.objects.create_wage(wages_employee=employee, wage_date=date1, start_time=time11,
                                        lunch_start=lun11, lunch_end=None, end_time=time22, hourly_rate=15.00)
        lunch1 = chm.time_diff(wage.lunch_start, wage.lunch_end)
        chm.assert_true_worker(self, Wage, wage)
        chm.assert_equals_worker(self, 86.25, wage.gross_wage)
        chm.assert_equals_worker(self, 5.75, wage.total_hours)
        chm.assert_false_non_instance_worker(self, wage.took_lunch)
        chm.assert_equals_worker(self, lunch1, wage.lunch_time)
        #print('test_wages_no_end_lunch: gross wage/hours/pay', wage.gross_wage, wage.total_hours, wage.hourly_rate)

    def test_wages_no_end_time(self):
        employee = Employee.objects.get(employee_id=9887)
        time11 = '09:00'
        time22 = '14:45'
        lun11 = '12:00'
        lun22 = '12:45'
        wage = Wage.objects.create_wage(wages_employee=employee, wage_date=date1, start_time=time11,
                                        lunch_start=lun11, lunch_end=lun22, end_time=None, hourly_rate=15.00)
        lunch1 = chm.time_diff(wage.lunch_start, wage.lunch_end)
        chm.assert_true_worker(self, Wage, wage)
        chm.assert_equals_worker(self, None, wage.gross_wage)
        chm.assert_equals_worker(self, None, wage.total_hours)
        chm.assert_equals_worker(self, lunch1, wage.lunch_time)
        #print('test_wages_no_end_time: gross wage/hours/pay', wage.gross_wage, wage.total_hours, wage.hourly_rate)
#endregion
