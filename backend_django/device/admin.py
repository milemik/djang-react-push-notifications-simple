from django.contrib import admin, messages
from .models import Device
from .selectors import get_push_uids
from .tasks import first_task_async, first_task_sync, send_push_request_task, send_push_aiohttp_task
from .utils import send_push


@admin.action(description="Send push notifications to all!")
def send_push_to_all(_modeladmin, request, _queryset) -> None:
    tokens = get_push_uids()
    success, failed = send_push(dry_run=True, tokens=tokens)

    messages.success(request, f"Success: {success}, Failed: {failed}")


@admin.action(description="Test send push notifications to all!")
def dry_run_send_push_to_all(_modeladmin, request, _queryset) -> None:
    """Users will not really receive notifications"""
    tokens = get_push_uids()
    success, failed = send_push(dry_run=True, tokens=tokens)

    messages.success(request, f"Success: {success}, Failed: {failed}")


@admin.action(description="Celery task ASYNC")
def send_push_task_async(_modeladmin, request, _queryset) -> None:
    first_task_async.delay()


@admin.action(description="Celery task sync")
def send_push_task_sync(_modeladmin, request, _queryset) -> None:
    first_task_sync.delay()


@admin.action(description="Send push request")
def send_push_request(_modeladmin, request, _queryset) -> None:
    send_push_request_task.delay()


@admin.action(description="Send push aiohttp")
def send_push_aiohttp_admin(_modeladmin, request, _queryset) -> None:
    send_push_aiohttp_task.delay()


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    actions = (
        send_push_to_all,
        dry_run_send_push_to_all,
        send_push_task_async,
        send_push_task_sync,
        send_push_request,
        send_push_aiohttp_admin
    )
