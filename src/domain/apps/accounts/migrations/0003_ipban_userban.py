# Generated by Django 4.2.3 on 2023-09-03 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0002_user_last_used_ip"),
    ]

    operations = [
        migrations.CreateModel(
            name="IPBan",
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
                ("until", models.DateTimeField()),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("Abusive", "Abusive"),
                            ("Racism", "Racism"),
                            ("Spam", "Spam"),
                            ("Suspicious Activity", "Suspicious Activity"),
                            ("OTHER", "Other"),
                        ],
                        default="Abusive",
                        max_length=20,
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=255, null=True),
                ),
                ("ip", models.GenericIPAddressField(unique=True, unpack_ipv4=True)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserBan",
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
                ("until", models.DateTimeField()),
                (
                    "reason",
                    models.CharField(
                        choices=[
                            ("Abusive", "Abusive"),
                            ("Racism", "Racism"),
                            ("Spam", "Spam"),
                            ("Suspicious Activity", "Suspicious Activity"),
                            ("OTHER", "Other"),
                        ],
                        default="Abusive",
                        max_length=20,
                    ),
                ),
                (
                    "description",
                    models.TextField(blank=True, max_length=255, null=True),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
    ]
