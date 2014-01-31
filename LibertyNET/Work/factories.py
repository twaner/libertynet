import factory
import factory.fuzzy
from Work.models import Job, Task, Ticket, Wage
from Common.factories import AddressFactory, ContactFactory
from Client.factories import ClientFactory
from Employee.factories import EmployeeFactory
from Employee.models import Employee
from Site.factories import SystemFactory

#region Factories

class JobFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Job
    job_id = 2323
    job_name = 'Job name'
    building_owner = 'Job building owner'
    job_client = factory.SubFactory(ClientFactory)
    job_address = factory.SubFactory(AddressFactory)
    #TODO m2m2
    #job_employee
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
    task_id = 4747
    task_ticket_id = factory.SubFactory(TicketFactory)
    task_name = 'Task name'
    task_created_date = '2013-12-21'
    task_creator = factory.SubFactory(EmployeeFactory)
    task_order = '3'
    is_task_completed = False
    task_completed_by = None
    task_completed_date = ''
    task_notes = 'Going Well'


class TicketFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Ticket
    ticket_id = 5454
    scheduled_date = '2014-1-21'
    scheduled_time =
    ticket_job = factory.SubFactory(JobFactory)
    ticket_system = factory.SubFactory(SystemFactory)
    description_work = 'Ticked description'
    technician_note = 'Technician notes'
    start_date = '2014-1-26'
    start_time = '1:21'
    end_date = None
    end_time = None
    task_site_contact = factory.SubFactory(ContactFactory)
    ticket_site_signature = None
    is_ticket_completed = False
    #TODO add m2m
    #ticket_employee


class WageFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Wage
    pass

#endregion