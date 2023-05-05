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


def send_push_sync(tokens: List[str], dry_run: bool = False) -> tuple[int, int]:
    notification = messaging.Notification(title="Hello test notification", body="Notification test")
    message = messaging.MulticastMessage(
        tokens=tokens,
        data={"score": "850", "time": "3:51"},
        notification=notification,
    )
    response = messaging.send_multicast(message, dry_run=dry_run)
    return response.success_count, response.failure_count


async def send_fb_push_async(tokens: List[str], dry_run: bool = False) -> None:
    res = await send_push_sync(tokens=tokens, dry_run=dry_run)
    print(res)


async def send_fb_async_many(tokens: list[str]) -> None:
    max_batch_size = 500  # max batch size can be up to 500
    tokens_batch = []
    tasks = set()
    for token in tokens:
        tokens_batch.append(token)
        if len(tokens_batch) >= max_batch_size:
            task = await asyncio.create_task(send_fb_push_async(tokens=tokens_batch))
            tasks.add(task)
            tokens_batch.clear()
    # await asyncio.gather(*tasks)


def print_responses_info(responses_returned: firebase_admin.messaging.BatchResponse) -> None:
    """Information that we can see from send_multicast message - sending batch"""
    for r in responses_returned.responses:
        print(f"EXCEPTION: {r.exception}\nMESSAGE ID: {r.message_id}MESSAGE SENT: {r.success}")
