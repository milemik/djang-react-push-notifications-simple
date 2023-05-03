import asyncio

import aiohttp
import requests
from django.conf import settings


def send_push_request(token: str):
    url = "https://fcm.googleapis.com/fcm/send"
    push_secret = settings.PUSH_SECRET_KEY
    header = {"Authorization": f"Bearer {push_secret}", "Content-Type": "application/json"}
    message_data = {"body": "Test", "title": "Test title"}
    payload = {"to": token, "data": message_data}

    return requests.post(url=url, headers=header, json=payload)


async def send_push_aiohttp(token: str):
    """
    more info here: https://firebase.google.com/docs/cloud-messaging/migrate-v1
    """
    url = "https://fcm.googleapis.com/fcm/send"
    # url_v1 = f"https://fcm.googleapis.com/v1/{project_id}/messages:send"
    push_secret = settings.PUSH_SECRET_KEY
    header = {"Authorization": f"Bearer {push_secret}", "Content-Type": "application/json"}
    message_data = {"body": "Test", "title": "Test title"}
    payload = {"to": token, "data": message_data}
    async with aiohttp.ClientSession() as session:
        response = await session.post(url=url, json=payload, headers=header)
        print(response)


async def send_push_many_aiohttp(tokens: list[str]) -> None:
    """
    ASYNC function to send multiple push notifications
    :param tokens: list of device tokens
    """
    tasks = set()
    for token in tokens:
        task = asyncio.create_task(send_push_aiohttp(token=token))
        tasks.add(task)
    await asyncio.gather(*tasks)
