from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Device
from .utils import add_device


class TestDeviceModel(TestCase):

    def setUp(self) -> None:
        self.device_uid = "djwadkwaodkakdowadoadwdoiwajdoiwajdoiwajdoiajdowaijwa"
        self.client = APIClient()
        self.add_device_url = reverse("add_device")

    def test_add_device(self):
        add_device(device_uid=self.device_uid)

        self.assertEqual(Device.objects.count(), 1)

    def test_add_device_api_init(self):
        response = self.client.post(self.add_device_url, {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_device_api_ok(self):
        response = self.client.post(self.add_device_url, {"push_uid": self.device_uid})

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
