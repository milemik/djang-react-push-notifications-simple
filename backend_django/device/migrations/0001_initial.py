# Generated by Django 4.1.5 on 2023-01-13 15:02

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Device",
            fields=[
                (
                    "uuid",
                    models.UUIDField(
                        default=uuid.UUID("78ea4251-b485-4c8d-ae68-c22ce514e7f3"),
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("last_update", models.DateTimeField(auto_now=True)),
                ("push_uid", models.CharField(max_length=255, unique=True)),
            ],
            options={
                "abstract": False,
            },
        ),
    ]