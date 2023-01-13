from django.urls import path

from .views import AddDeviceView

urlpatterns = [
    path("add_device/", AddDeviceView.as_view(), name="add_device"),
]