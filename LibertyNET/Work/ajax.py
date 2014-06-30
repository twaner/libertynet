import random
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from Equipment.models import Part
from Work.models import ClientEstimate
from Client.models import Client
from Site.models import Site

@dajaxice_register
def get_part(request, pk):
    """
    Gets details for a Part.
    @param request: request.
    @param pk: Pk of the Part.
    @return: json.
    """
    dajax = Dajax()
    part = Part.objects.get(pk=pk)
    dajax.assign('#idCost', 'innerHTML', str(part.cost))
    dajax.assign('#idFlat', 'innerHTML', str(part.flat_price))
    dajax.assign('#idLabor', 'innerHTML', str(part.labor))
    return dajax.json()

@dajaxice_register
def get_estimate_parts_details(request, pk, estimate_id):
    """
    Gets the Estimate_Parts object for an Estimate by Part Id
    @param request: request.
    @param pk: Pk of Part.
    @param estimate_id: Pk of Estimate.
    @return: json.
    """
    dajax = Dajax()
    estimate = ClientEstimate.objects.get(pk=estimate_id)
    if pk >= 1:
        est_parts = estimate.estimate_parts.filter(part_id=pk)
    print('value tester %s' % len(est_parts))
    if est_parts:
        ep = est_parts[0]
        dajax.assign('#id_quantity', 'value', str(ep.quantity))
        dajax.assign('#id_cost', 'value', str(ep.cost))
        dajax.assign('#id_final_cost', 'value', str(ep.final_cost))
        dajax.assign('#id_sub_total', 'value', str(ep.sub_total))
        dajax.assign('#id_profit', 'value', str(ep.profit))
        dajax.assign('#id_flat_total', 'value', str(ep.flat_total))
        dajax.assign('#id_total_labor', 'value', str(ep.total_labor))
    elif pk == 00000:
        dajax.assign('#id_quantity', 'value', str(0))
        dajax.assign('#id_cost', 'value', str(0))
        dajax.assign('#id_final_cost', 'value', str(0))
        dajax.assign('#id_sub_total', 'value', str(0))
        dajax.assign('#id_profit', 'value', str(0))
        dajax.assign('#id_flat_total', 'value', str(0))
        dajax.assign('#id_total_labor', 'value', str(0))
    else:
        dajax.assign('#id_quantity', 'value', str(0))
        dajax.assign('#id_cost', 'value', str(0))
        dajax.assign('#id_final_cost', 'value', str(0))
        dajax.assign('#id_sub_total', 'value', str(0))
        dajax.assign('#id_profit', 'value', str(0))
        dajax.assign('#id_flat_total', 'value', str(0))
        dajax.assign('#id_total_labor', 'value', str(0))
    return dajax.json()

@dajaxice_register
def get_sites(request, pk):
    dajax = Dajax()
    # get Sites
    site = list(Site.objects.filter(site_client=pk))
    # populate dropdown
    print('get_sites %s ' % site)
    out = []
    [out.append("<option value='#'>%s</option>" % option.get_address) for option in site]

    dajax.assign('#id_estimate_address', 'innerHTML', ''.join(out))

    return dajax.json()

@dajaxice_register
def get_estimate(request, pk):
    dajax = Dajax()
    est = ClientEstimate.objects.get(pk=pk)
    print('get_estimate %s ' % est)
    dajax.alert('Hello %s ' % est.job_name)
    # return simplejson.dumps({
    #     'message': est.name
    # })
    return dajax.json()


@dajaxice_register(method='GET')
def sayhello(request):
    dajax = Dajax()
    dajax.alert("Hello World!")
    return dajax.json()
    # return simplejson.dumps(
    #     {'message': 'Hello World'})

@dajaxice_register
def randomize(request):
    dajax = Dajax()
    dajax.assign('#result', 'value', random.randint(1, 10))
    return dajax.json()


@dajaxice_register
def assign_test(request):
    dajax = Dajax()
    dajax.assign('#box', 'innerHTML', 'Hello World!')
    dajax.add_css_class('div .alert', 'red')
    return dajax.json()

@dajaxice_register
def multiply(request, a, b):
    dajax = Dajax()
    result = int(a) * int(b)
    dajax.assign('#result', 'value', str(result))
    return dajax.json()

