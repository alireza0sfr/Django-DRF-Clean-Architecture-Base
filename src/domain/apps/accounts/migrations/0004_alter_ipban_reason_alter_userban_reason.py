# Generated by Django 4.2.3 on 2023-09-08 16:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0003_ipban_userban"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ipban",
            name="reason",
            field=models.CharField(
                choices=[
                    ("Abusive", "Abusive"),
                    ("Racism", "Racism"),
                    ("Spam", "Spam"),
                    ("Suspicious Activity", "Suspicious Activity"),
                    ("Honeypot", "Honeypot"),
                    ("OTHER", "Other"),
                ],
                default="Abusive",
                max_length=20,
            ),
        ),
        migrations.AlterField(
            model_name="userban",
            name="reason",
            field=models.CharField(
                choices=[
                    ("Abusive", "Abusive"),
                    ("Racism", "Racism"),
                    ("Spam", "Spam"),
                    ("Suspicious Activity", "Suspicious Activity"),
                    ("Honeypot", "Honeypot"),
                    ("OTHER", "Other"),
                ],
                default="Abusive",
                max_length=20,
            ),
        ),
    ]
