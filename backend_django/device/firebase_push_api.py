import asyncio

import aiohttp
import google.auth.transport.requests
import requests
from django.conf import settings
from google.oauth2 import service_account

import logging

logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/firebase.messaging", "https://www.googleapis.com/auth/cloud-platform"]


def send_push_request(token: str):
    url = "https://fcm.googleapis.com/fcm/send"
    push_secret = settings.PUSH_SECRET_KEY
    header = {"Authorization": f"Bearer {push_secret}", "Content-Type": "application/json"}
    message_data = {"body": "Test", "title": "Test title"}
    payload = {"to": token, "data": message_data}

    return requests.post(url=url, headers=header, json=payload)


async def send_push_aiohttp(tokens: list[str]):
    """
    Send Firebase push notifications using Legacy mode
    more info here: https://firebase.google.com/docs/cloud-messaging/migrate-v1
    """
    url = "https://fcm.googleapis.com/fcm/send"
    push_secret = settings.PUSH_SECRET_KEY
    header = {"Authorization": f"Bearer {push_secret}", "Content-Type": "application/json"}
    message_data = {"body": "Test", "title": "Test title"}
    payload = {"registration_ids": tokens, "data": message_data}
    async with aiohttp.ClientSession() as session:
        await session.post(url=url, json=payload, headers=header)


async def send_push_aiohttp_v1(token: str, access_token: str):
    """
    Send Firebase push notifications using HTTP_V1 - new suggested mode
    more info here: https://firebase.google.com/docs/cloud-messaging/migrate-v1

    NOTE: HTTP_V1 don't support sending group messages
    """
    project_id = settings.FIREBASE_PROJECT_ID
    url_v1 = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
    push_secret_v1 = access_token
    header = {"Authorization": f"Bearer {push_secret_v1}", "Content-Type": "application/json"}
    message_data = {"body": "Test", "title": "Test title"}
    payload = {"message": {"token": token, "data": message_data}}
    async with aiohttp.ClientSession() as session:
        await session.post(url=url_v1, json=payload, headers=header)


async def send_push_aiohttp_v1_group(tokens: list[str]):
    """
    Send Firebase push notifications using HTTP_V1 - new suggested mode
    more info here: https://firebase.google.com/docs/cloud-messaging/migrate-v1

    NOTE: HTTP_V1 don't support sending group messages
    """
    project_id = settings.FIREBASE_PROJECT_ID
    url_v1 = f"https://fcm.googleapis.com/v1/projects/{project_id}/messages:send"
    push_secret_v1 = get_access_token()
    header = {"Authorization": f"Bearer {push_secret_v1}", "Content-Type": "application/json"}
    message_data = {"body": "Test", "title": "Test title"}

    tasks = set()
    async with aiohttp.ClientSession() as session:
        for token in tokens:
            payload = {"message": {"token": token, "data": message_data}}
            task = asyncio.create_task(session.post(url=url_v1, json=payload, headers=header))
            tasks.add(task)
        result = await asyncio.gather(*tasks)
        logger.info(f"send_push_aiohttp_v1_group: {result}")
    return result


async def send_push_many_aiohttp(tokens: list[str]) -> None:
    """
    ASYNC function to send multiple push notifications
    :param tokens: list of device tokens
    """
    max_batch_size = 500  # Batch size can be up to 1000
    token_batch = []
    for token in tokens:
        token_batch.append(token)
        if len(token_batch) >= max_batch_size:
            await asyncio.create_task(send_push_aiohttp(tokens=token_batch))
            token_batch.clear()


async def send_push_many_aiohttp_v1(tokens: list[str]) -> None:
    """
    ASYNC function to send multiple push notifications
    :param tokens: list of device tokens
    NOTE: No batches possible
    """
    tasks = set()
    access_token = get_access_token()
    # print(access_token)
    for token in tokens:
        task = asyncio.create_task(send_push_aiohttp_v1(token=token, access_token=access_token))
        tasks.add(task)
    res = await asyncio.gather(*tasks)
    logger.info(f"send_push_many_aiohttp_v1: {res}")


def get_access_token() -> str:
    """
    Create access token for HTTP_V1 - API call
    https://googleapis.dev/python/google-auth/latest/user-guide.html#service-account-private-key-files
    """
    credentials = service_account.Credentials.from_service_account_info(
        settings.FIREBASE_CONF_DATA)

    scoped_credentials = credentials.with_scopes(SCOPES)

    request = google.auth.transport.requests.Request()
    scoped_credentials.refresh(request)
    return scoped_credentials.token
