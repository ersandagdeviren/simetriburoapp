# Generated by Django 4.2.5 on 2024-06-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("order", "0042_paymentreceipt_eur_amount_paymentreceipt_usd_amount"),
    ]

    operations = [
        migrations.AddField(
            model_name="paymentreceipt",
            name="transaction_number",
            field=models.CharField(blank=True, max_length=20, unique=True),
        ),
    ]
