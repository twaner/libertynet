__author__ = 'taiowawaner'
from Work.models import ClientEstimate, Estimate_Parts_Client, Estimate_Parts_Sales
from Work.estimate_engine import EstimateEngine
from Equipment.models import Part

# region Estimate Helpers


def create_estimate_step_one(form):
    job_name = form.cleaned_data['job_name']
    estimate_address = form.cleaned_data['estimate_address']
    date = form.cleaned_data['date']
    preparer = form.cleaned_data['preparer']
    is_capital_improvement = form.cleaned_data['is_capital_improvement']
    margin = form.cleaned_data['margin']

    estimate = ClientEstimate.objects.create_clientestimate(job_name=job_name, estimate_address=estimate_address,
                                                            date=date, preparer=preparer,
                                                            is_capital_improvement=is_capital_improvement,
                                                            margin=margin
    )
    return estimate


def add_part_helper(form, estimate):
    print('add_part_helper called')
    part_id = form.cleaned_data['part_id']
    quantity = form.cleaned_data['quantity']
    final_cost = form.cleaned_data['final_cost']
    cost = form.cleaned_data['cost']
    sub_total = form.cleaned_data['sub_total']
    profit = form.cleaned_data['profit']
    flat_total = form.cleaned_data['flat_total']
    total_labor = form.cleaned_data['total_labor']

    # Create new EstimateEngine
    ee = EstimateEngine(estimate)
    # Create the Estimate Parts obj
    is_new_part = ee.new_part_checker(part_id)
    # If True create else Update
    if is_new_part:
        est_parts = Estimate_Parts_Client.objects.create_estimate_parts(part_id, quantity, final_cost,
                                                                        cost, sub_total, profit, flat_total,
                                                                        total_labor)
        estimate.estimate_parts.add(est_parts)
        estimate.save()
        print('add_part_helper is_new_part!')
    else:
        # Update the Estimate Parts obj
        est_parts = update_part_helper(form, part_id, estimate)
    estimate = ee.set_estimate_totals()
    return estimate


def update_part_helper(form, part, estimate):
    p_list = estimate.estimate_parts.filter(part_id=part.id)
    est_parts = p_list[0]
    est_parts.part_id = form.cleaned_data['part_id']
    est_parts.quantity = form.cleaned_data['quantity']
    est_parts.final_cost = form.cleaned_data['final_cost']
    est_parts.cost = form.cleaned_data['cost'] * est_parts.quantity
    est_parts.sub_total = form.cleaned_data['sub_total']
    est_parts.profit = form.cleaned_data['profit']
    est_parts.flat_total = form.cleaned_data['flat_total']
    est_parts.total_labor = form.cleaned_data['total_labor']

    est_parts.save(update_fields=['part_id', 'quantity', 'final_cost', 'cost', 'sub_total',
                                  'profit', 'flat_total', 'total_labor'])
    return est_parts

# endregion


