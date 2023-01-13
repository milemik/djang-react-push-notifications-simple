from rest_framework import generics

from .models import Device
from .serializers import DeviceSerializer


class AddDeviceView(generics.CreateAPIView):
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
