from django.test import TestCase
from Equipment.factories import CameraFactory, DeviceFactory, PanelFactory, PartFactory
from Equipment.models import Camera, Device, Panel, Part

#region Factory Tests


class FactoryTestCases(TestCase):
    print('Starting Equipment FactoryTestCases...')

    def test_camera_factory(self):
        camera = CameraFactory()
        self.assertTrue(isinstance(camera, Camera), "CameraFactory is not Camera")

    def test_device_factory(self):
        device = DeviceFactory()
        self.assertTrue(isinstance(device, Device), "DeviceFactory is not Device")

    def test_panel_factory(self):
        panel = PanelFactory()
        self.assertTrue(isinstance(panel, Panel), "PanelFactory is not Panel")

    def test_part_factory(self):
        part = PartFactory()
        self.assertTrue(isinstance(part, Part), "PartFactory is not Part")

#endregion
