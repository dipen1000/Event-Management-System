# Generated by Django 5.0.7 on 2024-09-12 05:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0015_ticket_ticket_quantity"),
    ]

    operations = [
        migrations.AddField(
            model_name="attendee",
            name="email",
            field=models.EmailField(default=1, max_length=100),
            preserve_default=False,
        ),
    ]