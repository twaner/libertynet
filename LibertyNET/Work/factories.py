import factory
import factory.fuzzy
from Work.models import Job, Task, Ticket, Wage
from Common.factories import AddressFactory, ContactFactory
from Client.factories import ClientFactory
from Employee.factories import EmployeeFactory
from Employee.models import Employee
import Site.factories

#region Factories


class JobFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Job
    id = 2323
    name = 'Job name'
    building_owner = 456712
    job_client = factory.SubFactory(ClientFactory)
    job_address = factory.SubFactory(AddressFactory)

    @factory.post_generation
    def add_job_employee(self, create, extracted, **kwargs):
        if extracted and type(extracted) == type(Employee.objects.all()):
            self.job_employee = extracted
            self.save()
        else:
            if Employee.objects.all().count() < 1:
                EmployeeFactory.create()
            [self.job_employee.add(je) for je in Employee.objects.all()]


class TaskFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Task
    id = 4747
    task_ticket = factory.SubFactory('Work.factories.TicketFactory')
    name = 'Task name'
    created_date = '2013-12-21'
    creator = factory.SubFactory(EmployeeFactory)
    order = '3'
    is_task_completed = False
    task_employee = None
    completed_date = None
    notes = 'Going Well'


class TicketFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Ticket
    id = 5454
    scheduled_date = '2014-01-21'
    scheduled_time = '12:11'
    ticket_job = factory.SubFactory(JobFactory)
    ticket_system = factory.SubFactory(Site.factories.SystemFactory)
    description_work = 'Ticked description'
    notes = 'Technician notes'
    start_date = '2014-01-26'
    start_time = '14:21'
    end_date = None
    end_time = None
    ticket_contact = factory.SubFactory(ContactFactory)
    signature = None
    is_ticket_completed = False

    @factory.post_generation
    def add_ticket_employee(self, create, extracted, **kwargs):
        if extracted and type(extracted) == type(Employee.objects.all()):
            self.ticket_employee = extracted
            self.save()
        else:
            if Employee.objects.all().count() < 1:
                EmployeeFactory.create()
            [self.ticket_employee.add(je) for je in Employee.objects.all()]


class WageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Wage
    id = 4949
    wages_employee = factory.SubFactory(EmployeeFactory)
    wage_date = '2014-01-23'
    start_time = '01:21'
    lunch_start = '04:29'
    lunch_end = '05:00'
    end_time = '05:53'
    hourly_rate = 10.99
    gross_wage = 89.69
    total_hours = 8.4

#endregion