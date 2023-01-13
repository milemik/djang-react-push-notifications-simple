from typing import List

from .models import Device


def get_push_uids() -> List[str]:
    return list(Device.objects.values_list("push_uid", flat=True))
