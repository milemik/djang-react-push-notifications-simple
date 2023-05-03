from celery import shared_task


@shared_task
def first_task():
    return "OK"
