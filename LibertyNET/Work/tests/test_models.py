from django.test import TestCase
from Work.factories import JobFactory, TaskFactory, TicketFactory, WageFactory
from Work.models import Job, Task, Ticket, Wage

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

#endregion
