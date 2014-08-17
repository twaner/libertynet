__author__ = 'taiowawaner'
from Work.models import ClientEstimate, Estimate_Parts_Client, Estimate_Parts_Sales, Job, Ticket
from Work.estimate_engine import EstimateEngine
from Equipment.models import Part

# region Estimate Helpers


def create_estimate_helper(form):
    """
    Creates an Estimate object.
    @param form: form.
    @return: Estimate.
    """

    job_name = form.cleaned_data['job_name']
    estimate_address = form.cleaned_data['estimate_address']
    client = form.cleaned_data['estimate_client']
    date = form.cleaned_data['date']
    preparer = form.cleaned_data['preparer']
    is_capital_improvement = form.cleaned_data['is_capital_improvement']
    margin = form.cleaned_data['margin']
    margin_guidelines = form.cleaned_data['margin_guidelines']

    estimate = ClientEstimate.objects. \
        create_clientestimate(job_name=job_name, estimate_address=estimate_address,
                              date=date, preparer=preparer, estimate_client=client,
                              is_capital_improvement=is_capital_improvement,
                              margin=margin, margin_guidelines=margin_guidelines,
    )
    return estimate


def add_part_helper(form, estimate):
    """
    Adds a Part to an Estimate. Using the Estimate Engine.
    @param form: form.
    @param estimate: Estimate.
    @return: Updated Estimate.
    """
    part_id = form.cleaned_data['part_id']
    quantity = form.cleaned_data['quantity']
    final_cost = form.cleaned_data['final_cost']
    cost = form.cleaned_data['cost']
    sub_total = form.cleaned_data['sub_total']
    profit = form.cleaned_data['profit']
    flat_total = form.cleaned_data['flat_total']
    total_labor = form.cleaned_data['total_labor']

    ee = EstimateEngine(estimate)
    is_new_part = ee.new_part_checker(part_id)

    if is_new_part:
        est_parts = Estimate_Parts_Client.objects. \
            create_estimate_parts(part_id, quantity, final_cost,
                                  cost, sub_total, profit, flat_total,
                                  total_labor)
        estimate.estimate_parts.add(est_parts)
        estimate.save()
    else:
        update_part_helper(form, part_id, estimate)

    estimate = ee.set_estimate_totals()
    ee.get_aggregate_parts()

    return estimate


def update_part_helper(form, part, estimate):
    """
    Updates an Estimate Parts object.
    @param form: form.
    @param part: Part to be added.
    @param estimate: Estimate.
    @return: Estimate Parts object.
    """
    est_parts = estimate.estimate_parts.filter(part_id=part.id)[0]
    est_parts.quantity = form.cleaned_data['quantity']
    est_parts.final_cost = form.cleaned_data['final_cost']
    est_parts.cost = est_parts.part_id.cost * est_parts.quantity
    est_parts.sub_total = form.cleaned_data['sub_total']
    est_parts.profit = form.cleaned_data['profit']
    est_parts.flat_total = form.cleaned_data['flat_total']
    est_parts.total_labor = form.cleaned_data['total_labor']

    est_parts.save(update_fields=['quantity', 'final_cost', 'cost', 'sub_total',
                                  'profit', 'flat_total', 'total_labor'])


def update_estimate_helper(form, estimate):
    """
    Updates an Estimate to allow for custom pricing using
    the Estimate Engine.
    @param form: form.
    @param estimate: Estimate to be updated
    @return: Updated estimate.
    """
    estimate.job_name = form.cleaned_data['job_name']
    estimate.margin = form.cleaned_data['margin']
    estimate.listed_price = form.cleaned_data['listed_price']

    estimate.save(update_fields=['job_name', 'margin', 'listed_price'])
    ee = EstimateEngine(estimate)
    estimate = ee.set_estimate_totals()
    estimate.save()
    return estimate


# endregion

# region job


def create_job_helper(form):
    building_owner = 1
    name = form.cleaned_data['name']
    job_client = form.cleaned_data['job_client']
    job_address = form.cleaned_data['job_address']
    job_employee = form.cleaned_data['job_employee']
    job = Job.objects.create_job(name, building_owner, job_client, job_address,
                                 job_employee)
    return job


def update_job_helper(job, form):
    job.name = form.cleaned_data['name']
    job.job_employee = form.cleaned_data['job_employee']
    job.save(update_fields=['name', 'job_employee'])

    return job

#endregion

# region Ticket


def create_ticket_helper(form, notes, contact):
    scheduled_date = form.cleaned_data['scheduled_date']
    scheduled_time = form.cleaned_data['scheduled_time']
    ticket_job = form.cleaned_data['ticket_job']
    ticket_system = form.cleaned_data['ticket_system']
    description_work = form.cleaned_data['description_work']
    notes = notes
    start_date = form.cleaned_data['start_date']
    start_time = form.cleaned_data['start_time']
    end_date = form.cleaned_data['end_date']
    end_time = form.cleaned_data['end_time']
    ticket_contact = contact
    signature = form.cleaned_data['signature']
    is_ticket_completed = form.cleaned_data['is_ticket_completed']
    ticket_employee = form.cleaned_data['ticket_employee']

    ticket = Ticket.objects.create_ticket(scheduled_date=scheduled_date, scheduled_time=scheduled_time,
                                          ticket_job=ticket_job, ticket_system=ticket_system,
                                          description_work=description_work, notes=notes, start_date=start_date,
                                          start_time=start_time, end_date=end_date, ticket_contact=ticket_contact,
                                          signature=signature, is_ticket_completed=is_ticket_completed,
                                          ticket_employee=ticket_employee)
    return ticket

#endregion

