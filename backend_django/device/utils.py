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

    def send_push(self, dry_run: bool = False) -> Tuple[int, int]:
        notification = messaging.Notification(title="Hello test notification", body="Notification test")
        message = messaging.MulticastMessage(
            tokens=self.tokens,
            data={"score": "850", "time": "3:51"},
            notification=notification,
        )

        response = messaging.send_multicast(message, dry_run=dry_run)
        print_responses_info(responses_returned=response)

        return response.success_count, response.failure_count


def print_responses_info(responses_returned: firebase_admin.messaging.BatchResponse) -> None:
    for r in responses_returned.responses:
        print(r.exception)
        print(r.message_id)
        print(r.success)
