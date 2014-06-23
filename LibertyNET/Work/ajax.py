from django.utils import simplejson
import random
from dajaxice.decorators import dajaxice_register
from dajax.core import Dajax
from Equipment.models import Part
from Work.models import ClientEstimate

@dajaxice_register
def get_part(request, pk):
    print('ajax/get_part - CALLED! \nName: %s' % pk)
    dajax = Dajax()
    part = Part.objects.get(pk=pk)
    print('PART %s' % part)
    print('PartCOST %s ' % part.cost)
    # print('PART %s Cost: %s \nFlat %s \nLabor %s' % part, part.cost, part.flat_price, part.labor)
    # dajax.assign('#idCost', 'innerHTML', part.cost)
    # dajax.assign('#idFlat', 'innerHTML', part.flat_price)
    # dajax.assign('#idLabor', 'innerHTML', part.labor)
    print('get_part BEFORE return()')
    return dajax.json()

@dajaxice_register
def get_estimate(request, pk):
    dajax = Dajax()
    est = ClientEstimate.objects.get(pk=pk)
    dajax.alert('Hello %s ' % est.name)
    # return simplejson.dumps({
    #     'message': est.name
    # })

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

