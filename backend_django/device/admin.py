from django.contrib import admin, messages
from .models import Device
from .selectors import get_push_uids
from .utils import SendPushNotification


@admin.action(description="Send push notifications to all!")
def send_push_to_all(_modeladmin, request, _queryset) -> None:
    tokens = get_push_uids()
    push_init = SendPushNotification(tokens=tokens)
    success, failed = push_init.send_push()
    push_init.close_app()

    messages.success(request, f"Success: {success}, Failed: {failed}")


@admin.action(description="Test send push notifications to all!")
def dry_run_send_push_to_all(_modeladmin, request, _queryset) -> None:
    """Users will not really receive notifications"""
    tokens = get_push_uids()
    push_init = SendPushNotification(tokens=tokens)
    success, failed = push_init.send_push(dry_run=True)
    push_init.close_app()

    messages.success(request, f"Success: {success}, Failed: {failed}")


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    actions = (send_push_to_all, dry_run_send_push_to_all)
