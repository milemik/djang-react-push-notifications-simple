from django.test import TestCase

from .models import Device
from .services import add_device


class TestDeviceModel(TestCase):

    def setUp(self) -> None:
        self.device_uid = "djwadkwaodkakdowadoadwdoiwajdoiwajdoiwajdoiajdowaijwa"

    def test_add_device(self):
        add_device(device_uid=self.device_uid)

        self.assertEqual(Device.objects.count(), 1)
