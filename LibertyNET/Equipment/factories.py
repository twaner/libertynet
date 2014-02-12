import factory
import factory.fuzzy
from Equipment.models import Panel, Part, Camera, Device
import Vendor.factories as vf
import Common.factories as cf
import Site.factories

#region Factory


class PanelFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Panel
    #panel_id = 2929
    name = 'panel name'
    location = 'panel location'
    panel_id = factory.Sequence(lambda n: '%04d' % n, type=int)
    panel_manufacturer = factory.SubFactory(vf.ManufacturerFactory)
    user_manual = 'panel user manual'
    installation_manual = 'panel installation manual'


class DeviceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Device
    device_id = 3737
    name = 'device name'
    location = 'device base location'
    device_system_id = factory.SubFactory('Site.factories.SystemFactory')
    device_location = 'device location'
    device_function = 'device function'
    device_zone_id = factory.SubFactory('Site.factories.ZoneFactory')

    @factory.post_generation
    def add_camera_id(self, create, extracted, **kwargs):
        if extracted and type(extracted) == type(Camera.objects.all()):
            self.camera_id = extracted
            self.save()
        else:
            if Camera.objects.all().count() < 1:
                CameraFactory.create()
            [self.camera_id.add(je) for je in Camera.objects.all()]

    @factory.post_generation
    def add_part_id(self, create, extracted, **kwargs):
        if extracted and type(extracted) == type(Part.objects.all()):
            self.device_part_id = extracted
            self.save()
        else:
            if Part.objects.all().count() < 1:
                PartFactory.create()
            [self.device_part_id.add(pid) for pid in Part.objects.all()]


class PartFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Part
    id = 7676
    name = 'Part name'
    location = 'Part location'
    part_manufacturer = factory.SubFactory(vf.ManufacturerFactory)
    part_number = 54321
    type = factory.SubFactory(cf.GenreFactory)


class CameraFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Camera
    camera_id = 2525
    name = 'Camera name'
    location = 'Camera location'
    camera_system_id = factory.SubFactory('Site.factories.SystemFactory')
    notes = 'Camera notes'
    is_wireless = False

#endregion