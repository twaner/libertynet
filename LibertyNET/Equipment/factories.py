import factory
import factory.fuzzy
from Equipment.models import Panel, Part, Camera, Device
import Vendor.factories as vF
import Site.factories as sF
import Common.factories as cF

#region Factory


class PanelFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Panel
    panel_id = 2929
    name = 'panel name'
    location = 'panel location'
    panel_id = 3838
    panel_manufacturer = factory.SubFactory(vF.ManufacturerFactory)
    user_manual = 'panel user manual'
    installation_manual = 'panel installation manual'


class DeviceFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Device
    device_id = 3737
    name = 'device name'
    location = 'device base location'
    device_system_id = factory.SubFactory(sF.SystemFactory)
    device_location = 'device location'
    device_part_id = factory.SubFactory(PartFactory)
    device_function = 'device function'
    device_zone_id = factory.SubFactory(sF.ZoneFactory)
    # TODO add m2m for camera


class PartFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Part
    id = 7676
    name = 'Part name'
    location = 'Part location'
    part_manufacturer = factory.SubFactory(vF.ManufacturerFactory)
    part_number = 54321
    type = factory.SubFactory(cF.GenreFactory)


class CameraFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Camera
    camera_id = 2525
    name = 'Camera name'
    location = 'Camera location'
    camera_system_id = factory.SubFactory(sF.SystemFactory)
    notes = 'Camera notes'
    is_wireless = False

#endregion