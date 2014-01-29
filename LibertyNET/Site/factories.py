import factory
import factory.fuzzy
from Site.models import Site, Network
import Common.factories as comF
from Common.models import Call_List
import Client.factories as cF


class SiteFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Site
    site_id = 999
    site_client = factory.SubFactory(cF.ClientFactory)

    @factory.post_generation
    def add_call_list(self, create, extracted, **kwargs):
        if extracted and type(extracted) == type(Call_List.objects.all()):
            self.site_call_list = extracted
            self.save()
        else:
            if Call_List.objects.all().count() < 1:
                comF.Call_ListFactory.create()
            [self.site_call_list.add(sc) for sc in Call_List.objects.all()]


class NetworkFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Network
    network_id = 987
    router_address = '192.168.90.6969'
    router_user_name = 'Smith'
    router_password = 'secret'
    wifi_name = 'smithwifi'
    wifi_password = 'secretwifi'
    wifi_notes = 'wifi notes'
