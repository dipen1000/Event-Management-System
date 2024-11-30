# Generated by Django 5.0.7 on 2024-09-11 11:39

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("event", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Catering",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("address", models.CharField(max_length=50)),
                ("phone", models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="Equipments",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
            ],
        ),
        migrations.AlterField(
            model_name="eventcategory",
            name="event_name",
            field=models.CharField(
                choices=[
                    ("Conference", "CONFERENCE"),
                    ("Wedding", "WEDDING"),
                    ("Party", "PARTY"),
                    ("Reception", "RECEPTION"),
                    ("Concert", "CONCERT"),
                    ("Other", "OTHER"),
                ],
                max_length=10,
            ),
        ),
        migrations.CreateModel(
            name="Attendee",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("address", models.CharField(max_length=50)),
                ("phone", models.PositiveIntegerField()),
                ("registered_at", models.DateTimeField(auto_now_add=True)),
                (
                    "client",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attendees",
                        to="event.event",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Communication",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("message", models.TextField()),
                ("sent_at", models.DateTimeField(auto_now_add=True)),
                (
                    "attendee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="communications",
                        to="event.attendee",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="EventLogistics",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "transportation",
                    models.CharField(
                        choices=[
                            ("BUS", "Bus"),
                            ("CAR", "Car"),
                            ("VAN", "Van"),
                            ("SCORPIO", "Scorpio"),
                        ],
                        max_length=9,
                    ),
                ),
                (
                    "catering",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.catering"
                    ),
                ),
                ("equipments", models.ManyToManyField(to="event.equipments")),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.event"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Invoice",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("invoice_number", models.CharField(max_length=50, unique=True)),
                ("is_paid", models.BooleanField(default=False)),
                ("created_at", models.DateTimeField(default=django.utils.timezone.now)),
                (
                    "attendee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.attendee"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Payment",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "payment_mode",
                    models.CharField(
                        choices=[
                            ("ESEWA", "Esewa"),
                            ("KHALTI", "Khalti"),
                            ("IMEPAY", "ImePay"),
                            ("BANK_TRANSFER", "BankTransfer"),
                            ("OTHER", "Other"),
                        ],
                        default="Esewa",
                        max_length=15,
                    ),
                ),
                ("amount_paid", models.DecimalField(decimal_places=2, max_digits=10)),
                ("transaction_id", models.CharField(max_length=255, unique=True)),
                ("payment_date", models.DateTimeField(auto_now_add=True)),
                (
                    "invoice",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.invoice"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Reservation",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("reserved_at", models.DateTimeField(auto_now_add=True)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "attendee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.attendee"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.event"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Review",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rating", models.PositiveIntegerField()),
                ("feedback", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "attendee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reviews",
                        to="event.attendee",
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.event"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Ticket",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "ticket_type",
                    models.CharField(
                        choices=[("VIP", "Vip"), ("GENERAL", "General")],
                        default="General",
                        max_length=10,
                    ),
                ),
                ("issued_at", models.DateTimeField(auto_now_add=True)),
                (
                    "attendee",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="event.attendee"
                    ),
                ),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="tickets",
                        to="event.event",
                    ),
                ),
                (
                    "reservation",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="event.reservation",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="invoice",
            name="ticket",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to="event.ticket"
            ),
        ),
        migrations.CreateModel(
            name="Vendor",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=30)),
                ("email", models.EmailField(max_length=254, unique=True)),
                ("address", models.CharField(max_length=30)),
                ("phone", models.IntegerField()),
                (
                    "event",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT, to="event.event"
                    ),
                ),
            ],
        ),
        migrations.AlterUniqueTogether(
            name="invoice",
            unique_together={("attendee", "ticket")},
        ),
    ]
