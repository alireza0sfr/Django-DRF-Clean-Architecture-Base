# Generated by Django 4.2.3 on 2023-09-12 07:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="LoginAttempt",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                        unique=True,
                    ),
                ),
                ("created_date", models.DateTimeField(auto_now_add=True)),
                ("updated_date", models.DateTimeField(auto_now=True)),
                (
                    "username",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="username"
                    ),
                ),
                (
                    "password",
                    models.CharField(
                        blank=True, max_length=255, null=True, verbose_name="password"
                    ),
                ),
                (
                    "ip",
                    models.GenericIPAddressField(
                        blank=True, null=True, verbose_name="ip address"
                    ),
                ),
                (
                    "session_key",
                    models.CharField(
                        blank=True, max_length=50, null=True, verbose_name="session key"
                    ),
                ),
                (
                    "user_agent",
                    models.TextField(blank=True, null=True, verbose_name="user-agent"),
                ),
                ("path", models.TextField(blank=True, null=True, verbose_name="path")),
            ],
            options={
                "verbose_name": "Honeypot Login Attempt",
                "verbose_name_plural": "Honeypot Login Attempts",
                "ordering": ("-created_date",),
            },
        ),
    ]
