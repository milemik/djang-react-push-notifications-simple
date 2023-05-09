import asyncio

from celery import shared_task

from .firebase_push_api import send_push_request, send_push_many_aiohttp, send_push_many_aiohttp_v1, \
    send_push_aiohttp_v1_group
from .selectors import get_push_uids
from .utils import send_push_sync, send_fb_async_many


@shared_task
def first_task_sync():
    tokens = get_push_uids() * 1000
    tokens_batch = []
    batch_size = 500  # batch size can be up to 500
    for token in tokens:
        tokens_batch.append(token)
        if len(tokens_batch) >= batch_size:
            send_push_sync(tokens=tokens_batch)
            tokens_batch.clear()
    return "sync finished"


@shared_task
def send_fb_push_async():
    tokens = get_push_uids() * 1000  # 2*1000
    asyncio.run(send_fb_async_many(tokens=tokens))


@shared_task
def first_task_sync():
    tokens = get_push_uids() * 1000
    tokens_batch = []
    batch_size = 500  # batch size can be up to 500
    for token in tokens:
        tokens_batch.append(token)
        if len(tokens_batch) >= batch_size:
            send_push_sync(tokens=tokens_batch)
            tokens_batch.clear()
    return "sync finished"


@shared_task
def send_push_request_task():
    tokens = get_push_uids()
    for token in tokens:
        response = send_push_request(token=token)
        print(response.status_code)


@shared_task
def send_push_aiohttp_task_legacy():
    tokens = get_push_uids() * 1000
    asyncio.run(send_push_many_aiohttp(tokens=tokens))


@shared_task
def send_push_aiohttp_task():
    tokens = get_push_uids() * 1000
    asyncio.run(send_push_many_aiohttp_v1(tokens=tokens))


@shared_task
def send_push_aiohttp_v1_group_task():
    tokens = get_push_uids() * 100
    asyncio.run(send_push_aiohttp_v1_group(tokens=tokens))
