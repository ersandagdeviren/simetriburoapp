# Generated by Django 4.2.5 on 2024-06-22 11:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0043_paymentreceipt_transaction_number"),
    ]

    operations = [
        migrations.AlterField(
            model_name="paymentreceipt",
            name="date",
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
