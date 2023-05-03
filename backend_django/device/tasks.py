import asyncio

from celery import shared_task

from .firebase_push_api import send_push_request, send_push_many_aiohttp
from .selectors import get_push_uids
from .utils import send_to_many, send_push_sync


@shared_task
def first_task_async():
    tokens = get_push_uids() * 100
    asyncio.run(send_to_many(tokens=tokens))


@shared_task
def first_task_sync():
    tokens = get_push_uids() * 100
    for token in tokens:
        send_push_sync(tokens=[token])
    return "SYNC FINISHED!"


@shared_task
def send_push_request_task():
    tokens = get_push_uids() * 100
    for token in tokens:
        response = send_push_request(token=token)
        print(response.status_code)


@shared_task
def send_push_aiohttp_task():
    tokens = get_push_uids() * 100
    # send_push_many_aiohttp(tokens=tokens)
    asyncio.run(send_push_many_aiohttp(tokens=tokens))
