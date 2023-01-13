from typing import List, Tuple

from django.conf import settings

import firebase_admin
from firebase_admin import credentials, messaging

from .models import Device


def add_device(device_uid: str) -> Device:
    device = Device(push_uid=device_uid)
    device.save()
    return device


class SendPushNotification:
    def __init__(self, tokens: List[str]) -> None:
        cred = credentials.Certificate(settings.FIREBASE_CONF_DATA)
        self.app = firebase_admin.initialize_app(cred)
        self.tokens = tokens

    def close_app(self) -> None:
        firebase_admin.delete_app(self.app)

    def send_push(self) -> Tuple[int, int]:
        message = messaging.MulticastMessage(
            tokens=self.tokens,
            data={"score": "850", "time": "3:51"},
            notification=messaging.Notification(title="Hello test notification", body="Notification test"),
        )

        response = messaging.send_multicast(message)
        for resp in response.responses:
            print(resp.info)
        print(f"SUCCESS: {response.success_count}")
        print(f"FAILED:  {response.failure_count}")
        return response.success_count, response.failure_count
