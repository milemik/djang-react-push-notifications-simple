from .models import Device


def add_device(device_uid: str) -> Device:
    device = Device(push_uid=device_uid)
    device.save()
    return device
