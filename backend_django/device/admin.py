from django.contrib import admin, messages
from .models import Device
from .selectors import get_push_uids
from .tasks import first_task
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


@admin.action(description="Celery task")
def send_push_task(_modeladmin, request, _queryset) -> None:
    first_task.delay()


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    actions = (send_push_to_all, dry_run_send_push_to_all, send_push_task)
