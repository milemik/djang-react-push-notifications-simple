import asyncio
from typing import List

import firebase_admin
from django.conf import settings
from firebase_admin import credentials, messaging

from .models import Device

cred = credentials.Certificate(settings.FIREBASE_CONF_DATA)
app = firebase_admin.initialize_app(cred)


def add_device(device_uid: str) -> Device:
    device = Device(push_uid=device_uid)
    device.save()
    return device


async def send_push(tokens: List[str], dry_run: bool = False) -> None:
    notification = messaging.Notification(title="Hello test notification", body="Notification test")
    message = messaging.MulticastMessage(
        tokens=tokens,
        data={"score": "850", "time": "3:51"},
        notification=notification,
    )

    response = messaging.send_multicast(message, dry_run=dry_run)
    print_responses_info(responses_returned=response)

    # return response.success_count, response.failure_count


def send_push_sync(tokens: List[str], dry_run: bool = False) -> None:
    notification = messaging.Notification(title="Hello test notification", body="Notification test")
    message = messaging.MulticastMessage(
        tokens=tokens,
        data={"score": "850", "time": "3:51"},
        notification=notification,
    )
    response = messaging.send_multicast(message, dry_run=dry_run)
    print_responses_info(responses_returned=response)


async def send_to_many(tokens: list[str]) -> None:
    tasks = set()
    for token in tokens:
        task = asyncio.create_task(send_push(tokens=[token]))
        tasks.add(task)
    await asyncio.gather(*tasks)


def print_responses_info(responses_returned: firebase_admin.messaging.BatchResponse) -> None:
    for r in responses_returned.responses:
        print(f"EXCEPTION: {r.exception}\nMESSAGE ID: {r.message_id}MESSAGE SENT: {r.success}")
