from django.contrib import admin

from .models import Device
from .tasks import first_task_sync, send_push_request_task, send_push_aiohttp_task, send_push_aiohttp_task_legacy, \
    send_fb_push_async


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


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    actions = (
        send_push_task_sync,
        send_push_task_async,
        send_push_request,
        send_push_aiohttp_admin,
        send_push_aiohttp_admin_v1
    )
