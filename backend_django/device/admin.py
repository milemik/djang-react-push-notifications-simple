from django.contrib import admin
from django.db.models import QuerySet

from .models import Device
from .tasks import first_task_sync, send_push_request_task, send_push_aiohttp_task, send_push_aiohttp_task_legacy, \
    send_fb_push_async, send_push_aiohttp_v1_group_task
from .utils import subscribe_to_topic, TOPIC_NAME, unsubscribe_to_topic, send_message_to_topic

import logging

logger = logging.getLogger(__name__)


@admin.action(description="Celery task FB sync")
def send_push_task_sync(_modeladmin, request, _queryset) -> None:
    first_task_sync.delay()


@admin.action(description="Celery task FB ASYNC")
def send_push_task_async(_modeladmin, request, _queryset) -> None:
    send_fb_push_async.delay()


@admin.action(description="Send push request")
def send_push_request(_modeladmin, request, _queryset) -> None:
    send_push_request_task.delay()


@admin.action(description="Send push aiohttp")
def send_push_aiohttp_admin(_modeladmin, request, _queryset) -> None:
    send_push_aiohttp_task_legacy.delay()


@admin.action(description="Send push aiohttp V1")
def send_push_aiohttp_admin_v1(_modeladmin, request, _queryset) -> None:
    send_push_aiohttp_task.delay()


@admin.action(description="Send group push V1")
def send_group_push_v1(_modeladmin, request, _queryest) -> None:
    send_push_aiohttp_v1_group_task.delay()


@admin.action(description="Subscribe to topic")
def subscribe_to_topic_action(_modelamin, request, queryset: "QuerySet[Device]") -> None:
    device_tokens = list(queryset.values_list("push_uid", flat=True))
    success_count = subscribe_to_topic(tokens=device_tokens, topic_name=TOPIC_NAME)
    logger.info(f"subscribe_to_topic_action: {success_count}")


@admin.action(description="Unsubscribe to topic")
def unsubscribe_to_topic_action(_modelamin, request, queryset: "QuerySet[Device]") -> None:
    device_tokens = list(queryset.values_list("push_uid", flat=True))
    success_count = unsubscribe_to_topic(tokens=device_tokens, topic_name=TOPIC_NAME)
    logger.info(f"unsubscribe_to_topic_action: {success_count}")


@admin.action(description="Send message to topic")
def send_message_to_topic_action(_modeladmin, request, queryset: "QuerySet[Device]") -> None:
    send_message_to_topic(topic_name=TOPIC_NAME)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    actions = (
        send_push_task_sync,
        send_push_task_async,
        send_push_request,
        send_push_aiohttp_admin,
        send_push_aiohttp_admin_v1,
        send_group_push_v1,
        subscribe_to_topic_action,
        unsubscribe_to_topic_action,
        send_message_to_topic_action
    )
