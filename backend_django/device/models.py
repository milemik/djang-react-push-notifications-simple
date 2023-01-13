from django.db import models
import uuid


class UuidAbstractModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Device(UuidAbstractModel):
    push_uid = models.CharField(max_length=255, unique=True, blank=False, null=False)

    def __str__(self) -> str:
        return f"{self.push_uid}"[:8]
